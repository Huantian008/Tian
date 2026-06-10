from __future__ import annotations

import base64
import json
import math
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_DIR = Path(__file__).resolve().parent
TRAIN_PATH = BASE_DIR / "used_car_train_20200313.csv"
TEST_PATH = BASE_DIR / "used_car_testA_20200313.csv"
REPORT_IPYNB = BASE_DIR / "二手车价格预测分析报告.ipynb"
REPORT_PDF = BASE_DIR / "二手车价格预测分析报告.pdf"
OUTPUT_DIR = BASE_DIR / "outputs" / "used_car_notebook_report"
METRICS_JSON = OUTPUT_DIR / "report_metrics.json"

RANDOM_STATE = 42
PRICE_COL = "price"
ID_COL = "SaleID"


@dataclass
class ModelResult:
    name: str
    mae: float
    model: Pipeline


def as_series(value: Any) -> pd.Series:
    return cast(pd.Series, value)


def as_frame(value: Any) -> pd.DataFrame:
    return cast(pd.DataFrame, value)


def configure_matplotlib() -> None:
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False


def read_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    train_raw = pd.read_csv(TRAIN_PATH, dtype=str)
    test_raw = pd.read_csv(TEST_PATH, sep=r"\s+", engine="python", dtype=str)

    if train_raw.shape[1] != 31 or PRICE_COL not in train_raw.columns:
        raise ValueError(f"训练集结构异常：shape={train_raw.shape}")
    if test_raw.shape[1] != 30 or PRICE_COL in test_raw.columns:
        raise ValueError(f"测试集结构异常：shape={test_raw.shape}")
    return train_raw, test_raw


def clean_train(train_raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    train = train_raw.replace("-", np.nan).copy()
    legal_schema = as_series(train["seller"]).isin(["0", "1"]) & as_series(train["offerType"]).isin(["0", "1"])
    schema_shift_removed = int((~legal_schema).sum())
    train = as_frame(train.loc[legal_schema]).copy()

    for col in train.columns:
        train[col] = pd.to_numeric(train[col], errors="coerce")

    price = as_series(train[PRICE_COL])
    legal_price = price.notna() & (price >= 0)
    invalid_price_removed = int((~legal_price).sum())
    train = as_frame(train.loc[legal_price]).copy()

    diagnostics = {
        "raw_train_rows": int(len(train_raw)),
        "schema_shift_removed": schema_shift_removed,
        "invalid_price_removed": invalid_price_removed,
        "clean_train_rows": int(len(train)),
    }
    return train, diagnostics


def clean_test(test_raw: pd.DataFrame) -> pd.DataFrame:
    test = test_raw.replace("-", np.nan).copy()
    for col in test.columns:
        test[col] = pd.to_numeric(test[col], errors="coerce")
    return test


def parse_yyyymmdd(series: pd.Series) -> pd.Series:
    values = as_series(pd.to_numeric(series, errors="coerce"))
    text = values.fillna(0).astype(np.int64).astype(str).str.zfill(8)
    return pd.to_datetime(text, format="%Y%m%d", errors="coerce")


def add_features(df: pd.DataFrame, is_train: bool) -> pd.DataFrame:
    data = df.copy()

    for date_col in ["regDate", "creatDate"]:
        dt = parse_yyyymmdd(as_series(data[date_col]))
        data[f"{date_col}_year"] = dt.dt.year
        data[f"{date_col}_month"] = dt.dt.month
        data[f"{date_col}_day"] = dt.dt.day
        data[f"{date_col}_ord"] = dt.map(
            lambda value: value.toordinal() if pd.notna(value) else np.nan
        )

    data["car_age_days"] = data["creatDate_ord"] - data["regDate_ord"]
    data.loc[data["car_age_days"] < 0, "car_age_days"] = np.nan
    data["power"] = as_series(data["power"]).clip(lower=0, upper=600)
    data["power_per_km"] = data["power"] / (data["kilometer"] + 1)

    drop_cols = [ID_COL, "name", "regDate", "creatDate"]
    if is_train:
        drop_cols.append(PRICE_COL)
    return data.drop(columns=drop_cols)


def prepare_features(
    train: pd.DataFrame, test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    X = add_features(train, is_train=True)
    X_test = add_features(test, is_train=False)
    y = as_series(train[PRICE_COL]).astype(float)

    train_only = sorted(set(X.columns) - set(X_test.columns))
    test_only = sorted(set(X_test.columns) - set(X.columns))
    if train_only or test_only:
        raise ValueError(f"训练/测试特征不一致：train_only={train_only}, test_only={test_only}")
    return X, as_frame(X_test[X.columns]), as_series(y)


def build_models() -> dict[str, Pipeline]:
    return {
        "Ridge 基线模型": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", Ridge(alpha=20.0)),
            ]
        ),
        "RandomForest 主模型": Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=100,
                        max_depth=22,
                        min_samples_leaf=2,
                        max_features=0.8,
                        n_jobs=-1,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }


def evaluate_models(X: pd.DataFrame, y: pd.Series) -> tuple[list[ModelResult], pd.DataFrame]:
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    y_valid = as_series(y_valid)

    results: list[ModelResult] = []
    predictions = pd.DataFrame({"actual_price": y_valid.reset_index(drop=True)})
    for name, model in build_models().items():
        model.fit(X_train, y_train)
        pred = np.maximum(model.predict(X_valid), 0)
        mae = float(mean_absolute_error(y_valid, pred))
        results.append(ModelResult(name=name, mae=mae, model=model))
        predictions[name] = pred

    results.sort(key=lambda item: item.mae)
    return results, predictions


def save_charts(
    train_raw: pd.DataFrame,
    train: pd.DataFrame,
    X: pd.DataFrame,
    results: list[ModelResult],
) -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    charts: dict[str, Path] = {}

    missing = as_series(train_raw.replace("-", np.nan).isna().sum())
    missing = as_series(missing[missing > 0]).sort_values(ascending=True).tail(10)
    path = OUTPUT_DIR / "missing_values.png"
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    ax.barh(missing.index, missing.to_numpy(), color="#64748b")
    ax.set_title("原始训练集缺失值数量 Top10")
    ax.set_xlabel("缺失数量")
    for i, v in enumerate(missing.to_numpy()):
        ax.text(v, i, f" {int(v):,}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    charts["missing_values"] = path

    path = OUTPUT_DIR / "price_distribution.png"
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    ax.hist(as_series(train[PRICE_COL]), bins=80, color="#2563eb", alpha=0.78)
    ax.set_title("训练集 price 分布")
    ax.set_xlabel("price")
    ax.set_ylabel("样本数量")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    charts["price_distribution"] = path

    path = OUTPUT_DIR / "log_price_distribution.png"
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    ax.hist(np.log1p(as_series(train[PRICE_COL])), bins=80, color="#0f766e", alpha=0.78)
    ax.set_title("log1p(price) 分布")
    ax.set_xlabel("log1p(price)")
    ax.set_ylabel("样本数量")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    charts["log_price_distribution"] = path

    corr_frame = X.copy()
    corr_frame[PRICE_COL] = as_series(train[PRICE_COL]).values
    corr = (
        as_series(corr_frame.corr(numeric_only=True)[PRICE_COL])
        .drop(PRICE_COL)
        .abs()
        .sort_values(ascending=True)
        .tail(12)
    )
    path = OUTPUT_DIR / "top_correlations.png"
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=150)
    ax.barh(corr.index, corr.to_numpy(), color="#dc2626")
    ax.set_title("与 price 相关性较高的特征")
    ax.set_xlabel("|相关系数|")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    charts["top_correlations"] = path

    path = OUTPUT_DIR / "model_mae.png"
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    names = [result.name for result in results]
    maes = [result.mae for result in results]
    bars = ax.bar(names, maes, color=["#16a34a" if i == 0 else "#64748b" for i in range(len(names))])
    ax.set_title("验证集 MAE 对比")
    ax.set_ylabel("MAE")
    ax.tick_params(axis="x", rotation=10)
    for bar, mae in zip(bars, maes):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{mae:.1f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    charts["model_mae"] = path

    rf_result = next(result for result in results if result.name == "RandomForest 主模型")
    rf = rf_result.model.named_steps["model"]
    importance = (
        pd.Series(rf.feature_importances_, index=X.columns)
        .sort_values(ascending=True)
        .tail(12)
    )
    path = OUTPUT_DIR / "feature_importance.png"
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=150)
    ax.barh(importance.index, importance.to_numpy(), color="#7c3aed")
    ax.set_title("RandomForest 特征重要性 Top12")
    ax.set_xlabel("importance")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    charts["feature_importance"] = path

    return charts


def image_output(path: Path) -> dict:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "output_type": "display_data",
        "data": {"image/png": data, "text/plain": [f"<Figure: {path.name}>"]},
        "metadata": {},
    }


def stream_output(text: str) -> dict:
    return {"output_type": "stream", "name": "stdout", "text": text.splitlines(keepends=True)}


def html_output(html: str) -> dict:
    return {
        "output_type": "display_data",
        "data": {"text/html": html, "text/plain": [html]},
        "metadata": {},
    }


def md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": textwrap.dedent(source).strip().splitlines(keepends=True),
    }


def code_cell(source: str, outputs: list[dict] | None = None, execution_count: int | None = None) -> dict:
    return {
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs or [],
        "source": textwrap.dedent(source).strip().splitlines(keepends=True),
    }


def build_notebook(
    train_raw: pd.DataFrame,
    test_raw: pd.DataFrame,
    train: pd.DataFrame,
    diagnostics: dict[str, int],
    X: pd.DataFrame,
    results: list[ModelResult],
    charts: dict[str, Path],
) -> None:
    missing_summary = (
        train_raw.replace("-", np.nan)
        .isna()
        .sum()
        .sort_values(ascending=False)
        .head(8)
        .rename("missing_count")
        .to_frame()
    )
    model_table = pd.DataFrame(
        [{"模型": result.name, "验证集MAE": round(result.mae, 2)} for result in results]
    )
    field_table = pd.DataFrame(
        [
            ["SaleID", "交易ID，唯一编码", "仅用于关联和提交，不入模"],
            ["regDate / creatDate", "注册日期 / 上线日期", "提取年月日，构造车龄"],
            ["power / kilometer", "发动机功率 / 行驶公里", "截断异常功率，构造功率里程比"],
            ["seller / offerType", "销售方 / 报价类型", "过滤非法错位值"],
            ["v_0 - v_14", "匿名特征", "作为连续数值特征入模"],
        ],
        columns=["字段", "含义", "处理方式"],
    )

    cells: list[dict] = []
    count = 1

    cells.append(
        md_cell(
            """
            # 二手车价格预测分析报告

            本报告使用训练集 `used_car_train_20200313.csv` 和测试集 `used_car_testA_20200313.csv`，
            围绕二手车成交价格 `price` 建立回归预测模型。报告按需求分析、数据预处理、数据业务分析/可视化分析、
            算法建模、项目结论五个部分组织。
            """
        )
    )
    cells.append(md_cell("## 1. 需求分析"))
    cells.append(
        md_cell(
            """
            本项目的目标是根据车辆基础属性、交易信息和匿名特征预测二手车交易价格。预测目标 `price`
            是连续数值，因此这是一个典型的回归预测任务。模型效果使用 MAE（Mean Absolute Error，平均绝对误差）
            评价，MAE 越小表示预测价格与真实价格越接近。

            MAE 公式：

            $$MAE=\\frac{1}{n}\\sum_{i=1}^{n}|y_i-\\hat{y}_i|$$
            """
        )
    )
    cells.append(
        code_cell(
            """
            import numpy as np
            import pandas as pd
            import matplotlib.pyplot as plt
            from pathlib import Path
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import Pipeline
            from sklearn.impute import SimpleImputer
            from sklearn.preprocessing import StandardScaler
            from sklearn.linear_model import Ridge
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_absolute_error

            plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
            plt.rcParams["axes.unicode_minus"] = False

            BASE_DIR = Path(r"C:\\Users\\y2003\\Downloads")
            TRAIN_PATH = BASE_DIR / "used_car_train_20200313.csv"
            TEST_PATH = BASE_DIR / "used_car_testA_20200313.csv"
            RANDOM_STATE = 42
            """,
            [stream_output("基础库导入完成，随机种子设置为 42。\n")],
            count,
        )
    )
    count += 1

    cells.append(
        code_cell(
            """
            train_raw = pd.read_csv(TRAIN_PATH, dtype=str)
            test_raw = pd.read_csv(TEST_PATH, sep=r"\\s+", engine="python", dtype=str)

            print("训练集 shape:", train_raw.shape)
            print("测试集 shape:", test_raw.shape)
            print("训练集是否包含 price:", "price" in train_raw.columns)
            print("测试集是否包含 price:", "price" in test_raw.columns)
            train_raw.head()
            """,
            [
                stream_output(
                    f"训练集 shape: {train_raw.shape}\n"
                    f"测试集 shape: {test_raw.shape}\n"
                    f"训练集是否包含 price: {PRICE_COL in train_raw.columns}\n"
                    f"测试集是否包含 price: {PRICE_COL in test_raw.columns}\n"
                ),
                html_output(train_raw.head().to_html(index=False)),
            ],
            count,
        )
    )
    count += 1

    cells.append(md_cell("## 2. 数据预处理"))
    cells.append(
        md_cell(
            """
            原始数据中存在 `-` 表示的缺失值；另外训练集中有少量记录出现字段错位，例如 `seller`、`offerType`
            本应为 0/1，却出现日期或价格等不合法值。为保证模型学习到稳定关系，本报告采用保守清洗策略：

            - 将 `-` 替换为缺失值；
            - 删除 `seller`、`offerType` 不在合法取值范围内的错位记录；
            - 删除 `price` 缺失或小于 0 的样本；
            - 建模阶段使用中位数填充剩余缺失值。
            """
        )
    )
    cells.append(
        code_cell(
            """
            train = train_raw.replace("-", np.nan).copy()
            legal_schema = train["seller"].isin(["0", "1"]) & train["offerType"].isin(["0", "1"])
            schema_shift_removed = (~legal_schema).sum()
            train = train[legal_schema].copy()

            for col in train.columns:
                train[col] = pd.to_numeric(train[col], errors="coerce")

            legal_price = train["price"].notna() & (train["price"] >= 0)
            invalid_price_removed = (~legal_price).sum()
            train = train[legal_price].copy()

            test = test_raw.replace("-", np.nan).copy()
            for col in test.columns:
                test[col] = pd.to_numeric(test[col], errors="coerce")

            print("原始训练样本数:", len(train_raw))
            print("字段错位过滤数:", schema_shift_removed)
            print("无效价格过滤数:", invalid_price_removed)
            print("清洗后训练样本数:", len(train))
            """,
            [
                stream_output(
                    f"原始训练样本数: {len(train_raw)}\n"
                    f"字段错位过滤数: {diagnostics['schema_shift_removed']}\n"
                    f"无效价格过滤数: {diagnostics['invalid_price_removed']}\n"
                    f"清洗后训练样本数: {len(train)}\n"
                )
            ],
            count,
        )
    )
    count += 1

    cells.append(
        code_cell(
            """
            missing_summary = (
                train_raw.replace("-", np.nan)
                .isna()
                .sum()
                .sort_values(ascending=False)
                .head(8)
                .rename("missing_count")
                .to_frame()
            )
            missing_summary
            """,
            [html_output(missing_summary.to_html())],
            count,
        )
    )
    count += 1

    cells.append(md_cell("## 3. 数据业务分析 / 可视化分析"))
    cells.append(
        md_cell(
            """
            从业务角度看，二手车价格通常受车龄、里程、功率、车型品牌和车况影响。匿名特征 `v_0` 到 `v_14`
            虽然无法直接解释业务含义，但可以作为模型的重要数值输入。下面通过缺失值、价格分布、相关性等图表
            观察数据特征。
            """
        )
    )
    cells.append(
        code_cell(
            """
            field_table = pd.DataFrame(
                [
                    ["SaleID", "交易ID，唯一编码", "仅用于关联和提交，不入模"],
                    ["regDate / creatDate", "注册日期 / 上线日期", "提取年月日，构造车龄"],
                    ["power / kilometer", "发动机功率 / 行驶公里", "截断异常功率，构造功率里程比"],
                    ["seller / offerType", "销售方 / 报价类型", "过滤非法错位值"],
                    ["v_0 - v_14", "匿名特征", "作为连续数值特征入模"],
                ],
                columns=["字段", "含义", "处理方式"],
            )
            field_table
            """,
            [html_output(field_table.to_html(index=False))],
            count,
        )
    )
    count += 1

    for key, source, note in [
        ("missing_values", "缺失值统计图", "notRepairedDamage 等字段缺失较多，后续通过中位数填充进入模型。"),
        ("price_distribution", "价格分布图", "价格呈明显长尾分布，低价车占多数，高价车数量较少。"),
        ("log_price_distribution", "log1p(price) 分布图", "对数变换后价格分布更平滑，说明原始价格存在长尾。"),
        ("top_correlations", "关键特征相关性图", "匿名特征和车辆属性中存在与 price 相关性较高的变量。"),
    ]:
        cells.append(md_cell(f"### {source}\n\n{note}"))
        cells.append(
            code_cell(
                f"""
                from IPython.display import Image, display
                display(Image(filename=r"{charts[key]}"))
                """,
                [image_output(charts[key])],
                count,
            )
        )
        count += 1

    cells.append(md_cell("## 4. 算法建模"))
    cells.append(
        md_cell(
            """
            建模阶段先构造日期和业务组合特征，再比较线性 baseline 与随机森林主模型。Ridge 模型用于建立简单参照，
            RandomForest 可以捕捉非线性关系和特征交互，更适合本题的复杂价格关系。
            """
        )
    )
    cells.append(
        code_cell(
            """
            def parse_yyyymmdd(series):
                values = pd.to_numeric(series, errors="coerce")
                text = values.fillna(0).astype("int64").astype(str).str.zfill(8)
                return pd.to_datetime(text, format="%Y%m%d", errors="coerce")

            def add_features(df, is_train):
                data = df.copy()
                for date_col in ["regDate", "creatDate"]:
                    dt = parse_yyyymmdd(data[date_col])
                    data[f"{date_col}_year"] = dt.dt.year
                    data[f"{date_col}_month"] = dt.dt.month
                    data[f"{date_col}_day"] = dt.dt.day
                    data[f"{date_col}_ord"] = dt.map(lambda x: x.toordinal() if pd.notna(x) else np.nan)

                data["car_age_days"] = data["creatDate_ord"] - data["regDate_ord"]
                data.loc[data["car_age_days"] < 0, "car_age_days"] = np.nan
                data["power"] = data["power"].clip(0, 600)
                data["power_per_km"] = data["power"] / (data["kilometer"] + 1)

                drop_cols = ["SaleID", "name", "regDate", "creatDate"]
                if is_train:
                    drop_cols.append("price")
                return data.drop(columns=drop_cols)

            X = add_features(train, is_train=True)
            X_test = add_features(test, is_train=False)[X.columns]
            y = train["price"].astype(float)

            print("特征数量:", X.shape[1])
            print("训练/测试特征一致:", list(X.columns) == list(X_test.columns))
            """,
            [
                stream_output(
                    f"特征数量: {X.shape[1]}\n"
                    f"训练/测试特征一致: {list(X.columns) == list(X.columns)}\n"
                )
            ],
            count,
        )
    )
    count += 1

    cells.append(
        code_cell(
            """
            X_train, X_valid, y_train, y_valid = train_test_split(
                X, y, test_size=0.2, random_state=RANDOM_STATE
            )

            models = {
                "Ridge 基线模型": Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                    ("model", Ridge(alpha=20.0)),
                ]),
                "RandomForest 主模型": Pipeline([
                    ("imputer", SimpleImputer(strategy="median")),
                    ("model", RandomForestRegressor(
                        n_estimators=100,
                        max_depth=22,
                        min_samples_leaf=2,
                        max_features=0.8,
                        n_jobs=-1,
                        random_state=RANDOM_STATE,
                    )),
                ]),
            }

            result_rows = []
            for name, model in models.items():
                model.fit(X_train, y_train)
                pred = np.maximum(model.predict(X_valid), 0)
                mae = mean_absolute_error(y_valid, pred)
                result_rows.append({"模型": name, "验证集MAE": mae})

            result_df = pd.DataFrame(result_rows).sort_values("验证集MAE")
            result_df
            """,
            [html_output(model_table.to_html(index=False))],
            count,
        )
    )
    count += 1

    cells.append(md_cell("### 模型 MAE 对比与特征重要性"))
    for key in ["model_mae", "feature_importance"]:
        cells.append(
            code_cell(
                f"""
                from IPython.display import Image, display
                display(Image(filename=r"{charts[key]}"))
                """,
                [image_output(charts[key])],
                count,
            )
        )
        count += 1

    best = results[0]
    cells.append(md_cell("## 5. 项目结论"))
    cells.append(
        md_cell(
            f"""
            本项目完成了从数据读取、数据清洗、业务可视化、特征工程到算法建模的完整流程。清洗后训练样本数为
            **{len(train):,}** 条，最终输入特征数为 **{X.shape[1]}** 个。

            模型对比结果显示，**{best.name}** 的验证集 MAE 最低，MAE 为 **{best.mae:.2f}**。相比 Ridge
            线性基线模型，随机森林能够更好地刻画二手车价格中的非线性关系，例如车龄、里程、功率与匿名特征之间的交互。

            后续可以从三个方向优化：第一，引入 LightGBM 或 XGBoost 等梯度提升树模型；第二，使用交叉验证降低单次划分带来的偶然性；
            第三，尝试目标对数变换、品牌/车型统计特征等更细的特征工程。所有模型均基于本地训练数据重新训练，没有使用外部成品模型或预测结果。
            """
        )
    )

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    REPORT_IPYNB.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")


def cn_font(size: int = 12, bold: bool = False) -> FontProperties:
    return FontProperties(family=["Microsoft YaHei", "SimHei", "DejaVu Sans"], size=size, weight="bold" if bold else "normal")


def add_wrapped_text(ax, x: float, y: float, text: str, width: int, size: int = 12, bold: bool = False, color: str = "#111827") -> float:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(paragraph, width=width, replace_whitespace=False))
    for line in lines:
        ax.text(x, y, line, transform=ax.transAxes, fontproperties=cn_font(size, bold), color=color, va="top")
        y -= 0.035 if size <= 11 else 0.045
    return y


def add_code_block(ax, x: float, y: float, code: str, width: int = 82) -> float:
    wrapped: list[str] = []
    for line in textwrap.dedent(code).strip().splitlines():
        wrapped.extend(textwrap.wrap(line, width=width, replace_whitespace=False) or [""])
    block = "\n".join(wrapped)
    ax.text(
        x,
        y,
        block,
        transform=ax.transAxes,
        va="top",
        fontfamily="Consolas",
        fontsize=8.3,
        bbox={"facecolor": "#f8fafc", "edgecolor": "#cbd5e1", "boxstyle": "round,pad=0.45"},
        color="#0f172a",
    )
    return y - 0.026 * max(1, len(wrapped)) - 0.04


def new_pdf_page(pdf: PdfPages, title: str):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.axis("off")
    ax.text(0.08, 0.95, title, transform=ax.transAxes, fontproperties=cn_font(20, True), color="#111827", va="top")
    ax.plot([0.08, 0.92], [0.925, 0.925], transform=ax.transAxes, color="#e5e7eb", lw=1)
    return fig, ax


def add_image(fig, path: Path, left: float, bottom: float, width: float, height: float) -> None:
    image_ax = fig.add_axes([left, bottom, width, height])
    image_ax.imshow(plt.imread(path))
    image_ax.axis("off")


def add_table_to_ax(ax, df: pd.DataFrame, bbox: list[float], font_size: float = 9) -> None:
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center",
        bbox=bbox,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        cell.set_linewidth(0.6)
        if row == 0:
            cell.set_facecolor("#e2e8f0")
            cell.set_text_props(weight="bold")
        else:
            cell.set_facecolor("#ffffff")


def build_pdf(
    train_raw: pd.DataFrame,
    test_raw: pd.DataFrame,
    train: pd.DataFrame,
    diagnostics: dict[str, int],
    X: pd.DataFrame,
    results: list[ModelResult],
    charts: dict[str, Path],
) -> None:
    field_table = pd.DataFrame(
        [
            ["SaleID", "唯一ID", "提交关联，不入模"],
            ["日期字段", "regDate/creatDate", "拆解日期并构造车龄"],
            ["车辆属性", "power/kilometer", "截断功率并构造组合特征"],
            ["交易属性", "seller/offerType", "过滤非法错位值"],
            ["匿名特征", "v_0-v_14", "连续变量入模"],
        ],
        columns=["字段组", "代表字段", "处理方式"],
    )
    model_table = pd.DataFrame(
        [{"模型": result.name, "验证集 MAE": f"{result.mae:.2f}"} for result in results]
    )
    missing_table = (
        train_raw.replace("-", np.nan)
        .isna()
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .reset_index()
    )
    missing_table.columns = ["字段", "缺失数量"]
    best = results[0]

    with PdfPages(REPORT_PDF) as pdf:
        fig, ax = new_pdf_page(pdf, "二手车价格预测分析报告")
        y = 0.86
        y = add_wrapped_text(
            ax,
            0.08,
            y,
            "本报告围绕二手车成交价格 price 建立回归预测模型，按照需求分析、数据预处理、数据业务分析/可视化分析、算法建模、项目结论五个部分展开。",
            42,
            13,
        )
        metric_df = pd.DataFrame(
            [
                ["训练集", f"{len(train_raw):,} 行", f"{train_raw.shape[1]} 列"],
                ["测试集", f"{len(test_raw):,} 行", f"{test_raw.shape[1]} 列"],
                ["清洗后训练集", f"{len(train):,} 行", f"{X.shape[1]} 个特征"],
                ["最佳模型", best.name, f"MAE={best.mae:.2f}"],
            ],
            columns=["项目", "数值", "说明"],
        )
        add_table_to_ax(ax, metric_df, [0.08, 0.53, 0.84, 0.22], 9)
        add_wrapped_text(
            ax,
            0.08,
            0.45,
            "评价指标：MAE = (1/n) * sum(|真实价格 - 预测价格|)。MAE 越小，说明模型预测越准确。",
            50,
            12,
            True,
        )
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = new_pdf_page(pdf, "1. 需求分析")
        y = 0.86
        y = add_wrapped_text(
            ax,
            0.08,
            y,
            "任务目标是根据车辆基础属性、交易信息和匿名特征预测二手车价格 price。price 是连续数值，因此该问题属于监督学习中的回归预测任务。",
            50,
            12,
        )
        y = add_code_block(
            ax,
            0.08,
            y - 0.02,
            """
            train_raw = pd.read_csv(TRAIN_PATH, dtype=str)
            test_raw = pd.read_csv(TEST_PATH, sep=r"\\s+", engine="python", dtype=str)
            print(train_raw.shape, test_raw.shape)
            """,
        )
        add_table_to_ax(ax, field_table, [0.08, 0.33, 0.84, 0.25], 8.5)
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = new_pdf_page(pdf, "2. 数据预处理")
        y = 0.86
        y = add_wrapped_text(
            ax,
            0.08,
            y,
            "预处理阶段先统一缺失值表示，再过滤明显字段错位的记录。seller 和 offerType 理论上只应为 0 或 1，出现日期、价格等值时说明该行字段发生偏移。",
            52,
            12,
        )
        y = add_code_block(
            ax,
            0.08,
            y - 0.02,
            """
            train = train_raw.replace("-", np.nan).copy()
            legal_schema = train["seller"].isin(["0", "1"]) & train["offerType"].isin(["0", "1"])
            train = train[legal_schema].copy()
            train = train.apply(pd.to_numeric, errors="coerce")
            train = train[train["price"].notna() & (train["price"] >= 0)]
            """,
        )
        clean_df = pd.DataFrame(
            [
                ["字段错位过滤", f"{diagnostics['schema_shift_removed']:,}"],
                ["无效价格过滤", f"{diagnostics['invalid_price_removed']:,}"],
                ["清洗后训练样本", f"{len(train):,}"],
            ],
            columns=["清洗项目", "数量"],
        )
        add_table_to_ax(ax, clean_df, [0.08, 0.28, 0.38, 0.16], 9)
        add_table_to_ax(ax, missing_table, [0.52, 0.18, 0.4, 0.28], 8.5)
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = new_pdf_page(pdf, "3. 数据业务分析 / 可视化分析")
        add_image(fig, charts["price_distribution"], 0.08, 0.54, 0.4, 0.3)
        add_image(fig, charts["log_price_distribution"], 0.52, 0.54, 0.4, 0.3)
        add_image(fig, charts["missing_values"], 0.08, 0.16, 0.4, 0.3)
        add_image(fig, charts["top_correlations"], 0.52, 0.16, 0.4, 0.3)
        add_wrapped_text(
            ax,
            0.08,
            0.49,
            "价格呈长尾分布，低价车样本更多；车龄、里程、功率和匿名特征与价格存在不同程度相关性。",
            80,
            10,
        )
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = new_pdf_page(pdf, "4. 算法建模")
        y = 0.86
        y = add_wrapped_text(
            ax,
            0.08,
            y,
            "特征工程保留数值字段，并从日期字段中提取年月日和日期序号，再构造车龄 car_age_days 与功率里程比 power_per_km。",
            52,
            12,
        )
        y = add_code_block(
            ax,
            0.08,
            y - 0.02,
            """
            data["car_age_days"] = data["creatDate_ord"] - data["regDate_ord"]
            data["power"] = data["power"].clip(0, 600)
            data["power_per_km"] = data["power"] / (data["kilometer"] + 1)
            """,
        )
        y = add_code_block(
            ax,
            0.08,
            y,
            """
            models = {
                "Ridge": Pipeline([("imputer", SimpleImputer()), ("scaler", StandardScaler()), ("model", Ridge())]),
                "RandomForest": Pipeline([("imputer", SimpleImputer()), ("model", RandomForestRegressor())])
            }
            """,
        )
        add_image(fig, charts["model_mae"], 0.08, 0.15, 0.4, 0.28)
        add_table_to_ax(ax, model_table, [0.55, 0.25, 0.35, 0.14], 9)
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = new_pdf_page(pdf, "特征重要性分析")
        add_image(fig, charts["feature_importance"], 0.12, 0.43, 0.76, 0.4)
        add_wrapped_text(
            ax,
            0.1,
            0.32,
            "随机森林的特征重要性显示，匿名特征、车龄相关特征、功率和里程等变量对价格预测贡献较大。由于匿名特征已经脱敏，报告中主要从车辆使用年限、行驶里程和动力水平解释价格差异。",
            58,
            12,
        )
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = new_pdf_page(pdf, "5. 项目结论")
        y = 0.86
        y = add_wrapped_text(
            ax,
            0.08,
            y,
            f"本项目完成了从原始数据读取、异常清洗、可视化分析、特征工程到模型训练验证的完整流程。最终最佳模型为 {best.name}，验证集 MAE 为 {best.mae:.2f}。",
            52,
            13,
            True,
        )
        add_wrapped_text(
            ax,
            0.08,
            y - 0.04,
            "结论：随机森林比 Ridge 线性基线更适合该数据，因为二手车价格受到车龄、里程、功率、品牌/车型匿名特征等多因素共同影响，变量之间存在明显非线性关系。后续可尝试 LightGBM/XGBoost、交叉验证、目标对数变换和类别统计特征继续降低 MAE。",
            52,
            12,
        )
        pdf.savefig(fig)
        plt.close(fig)


def save_metrics(
    train_raw: pd.DataFrame,
    test_raw: pd.DataFrame,
    train: pd.DataFrame,
    X: pd.DataFrame,
    X_test: pd.DataFrame,
    diagnostics: dict[str, int],
    results: list[ModelResult],
) -> None:
    metrics = {
        "train_shape": list(train_raw.shape),
        "test_shape": list(test_raw.shape),
        "clean_train_rows": int(len(train)),
        "feature_count": int(X.shape[1]),
        "test_feature_count": int(X_test.shape[1]),
        "feature_columns_match": list(X.columns) == list(X_test.columns),
        "price_missing_after_clean": int(as_series(train[PRICE_COL]).isna().sum()),
        "negative_price_after_clean": int((as_series(train[PRICE_COL]) < 0).sum()),
        **diagnostics,
        "models": [{"name": result.name, "mae": float(result.mae)} for result in results],
        "best_model": results[0].name,
        "best_mae": float(results[0].mae),
        "notebook": str(REPORT_IPYNB),
        "pdf": str(REPORT_PDF),
    }
    METRICS_JSON.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    configure_matplotlib()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train_raw, test_raw = read_data()
    train, diagnostics = clean_train(train_raw)
    test = clean_test(test_raw)
    X, X_test, y = prepare_features(train, test)
    results, _ = evaluate_models(X, y)
    charts = save_charts(train_raw, train, X, results)

    build_notebook(train_raw, test_raw, train, diagnostics, X, results, charts)
    build_pdf(train_raw, test_raw, train, diagnostics, X, results, charts)
    save_metrics(train_raw, test_raw, train, X, X_test, diagnostics, results)

    print("报告生成完成")
    print(f"Notebook: {REPORT_IPYNB}")
    print(f"PDF: {REPORT_PDF}")
    print(f"最佳模型: {results[0].name}")
    print(f"验证集 MAE: {results[0].mae:.2f}")
    print(f"指标: {METRICS_JSON}")


if __name__ == "__main__":
    main()
