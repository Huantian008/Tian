"""
二手车价格预测：数据清洗、特征工程、建模、预测文件和精简 PPT 生成。

运行：
    python used_car_price_prediction.py

输出：
    used_car_price_submission.csv
    二手车价格预测_精简报告.pptx
    outputs/used_car_price_prediction/*.png
"""

from __future__ import annotations

import json
import math
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=UserWarning)


BASE_DIR = Path(__file__).resolve().parent
TRAIN_PATH = BASE_DIR / "used_car_train_20200313.csv"
TEST_PATH = BASE_DIR / "used_car_testA_20200313.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "used_car_price_prediction"
SUBMISSION_PATH = BASE_DIR / "used_car_price_submission.csv"
METRICS_PATH = OUTPUT_DIR / "metrics.json"

RANDOM_STATE = 42
PRICE_COL = "price"
ID_COL = "SaleID"


@dataclass
class ModelResult:
    name: str
    mae: float
    model: object


def as_series(value: Any) -> pd.Series:
    return cast(pd.Series, value)


def as_frame(value: Any) -> pd.DataFrame:
    return cast(pd.DataFrame, value)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read the train/test files with their actual delimiters."""
    if not TRAIN_PATH.exists():
        raise FileNotFoundError(f"训练集不存在：{TRAIN_PATH}")
    if not TEST_PATH.exists():
        raise FileNotFoundError(f"测试集不存在：{TEST_PATH}")

    train = pd.read_csv(TRAIN_PATH, dtype=str)
    test = pd.read_csv(TEST_PATH, sep=r"\s+", engine="python", dtype=str)

    if train.shape[1] != 31 or PRICE_COL not in train.columns:
        raise ValueError(f"训练集列结构异常：shape={train.shape}, columns={list(train.columns)}")
    if test.shape[1] != 30 or PRICE_COL in test.columns:
        raise ValueError(f"测试集列结构异常：shape={test.shape}, columns={list(test.columns)}")
    return train, test


def clean_train(train_raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Clean rows that are unusable because of missing values or field shifts."""
    before = len(train_raw)
    train = train_raw.replace("-", np.nan).copy()

    legal_schema = as_series(train["seller"]).isin(["0", "1"]) & as_series(train["offerType"]).isin(["0", "1"])
    schema_removed = int((~legal_schema).sum())
    train = as_frame(train.loc[legal_schema]).copy()

    for col in train.columns:
        train[col] = pd.to_numeric(train[col], errors="coerce")

    price = as_series(train[PRICE_COL])
    valid_price = price.notna() & (price >= 0)
    invalid_price_removed = int((~valid_price).sum())
    train = as_frame(train.loc[valid_price]).copy()

    diagnostics = {
        "raw_train_rows": before,
        "schema_shift_removed": schema_removed,
        "invalid_price_removed": invalid_price_removed,
        "clean_train_rows": len(train),
    }
    return train, diagnostics


def clean_test(test_raw: pd.DataFrame) -> pd.DataFrame:
    test = test_raw.replace("-", np.nan).copy()
    for col in test.columns:
        test[col] = pd.to_numeric(test[col], errors="coerce")
    return test


def _parse_yyyymmdd(series: pd.Series) -> pd.Series:
    cleaned = as_series(pd.to_numeric(series, errors="coerce"))
    text = cleaned.fillna(0).astype(np.int64).astype(str).str.zfill(8)
    return pd.to_datetime(text, format="%Y%m%d", errors="coerce")


def add_features(df: pd.DataFrame, is_train: bool) -> pd.DataFrame:
    data = df.copy()

    for date_col in ["regDate", "creatDate"]:
        dt = _parse_yyyymmdd(as_series(data[date_col]))
        data[f"{date_col}_year"] = dt.dt.year
        data[f"{date_col}_month"] = dt.dt.month
        data[f"{date_col}_day"] = dt.dt.day
        data[f"{date_col}_ord"] = dt.map(lambda value: value.toordinal() if pd.notna(value) else np.nan)

    data["car_age_days"] = data["creatDate_ord"] - data["regDate_ord"]
    data.loc[data["car_age_days"] < 0, "car_age_days"] = np.nan
    data["power"] = as_series(data["power"]).clip(lower=0, upper=600)
    data["power_per_km"] = data["power"] / (data["kilometer"] + 1)

    drop_cols = [ID_COL, "name", "regDate", "creatDate"]
    if is_train:
        drop_cols.append(PRICE_COL)
    return data.drop(columns=drop_cols)


def prepare_features(train: pd.DataFrame, test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    X = add_features(train, is_train=True)
    X_test = add_features(test, is_train=False)
    y = as_series(train[PRICE_COL]).astype(float)

    missing_train = sorted(set(X.columns) - set(X_test.columns))
    missing_test = sorted(set(X_test.columns) - set(X.columns))
    if missing_train or missing_test:
        raise ValueError(f"训练/测试特征不一致：train_only={missing_train}, test_only={missing_test}")

    X_test = as_frame(X_test[X.columns])
    return X, X_test, as_series(y)


def make_models() -> dict[str, Pipeline]:
    models: dict[str, Pipeline] = {
        "Ridge 基线模型": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", Ridge(alpha=20.0)),
            ]
        ),
        "RandomForest 主模型": Pipeline(
            steps=[
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

    try:
        from lightgbm import LGBMRegressor  # type: ignore

        models["LightGBM 可选增强"] = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    LGBMRegressor(
                        n_estimators=500,
                        learning_rate=0.05,
                        num_leaves=64,
                        subsample=0.85,
                        colsample_bytree=0.85,
                        objective="regression_l1",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        )
    except Exception:
        pass
    return models


def evaluate_models(X: pd.DataFrame, y: pd.Series) -> tuple[list[ModelResult], pd.DataFrame, pd.Series]:
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )
    X_valid = as_frame(X_valid)
    y_valid = as_series(y_valid)

    results: list[ModelResult] = []
    for name, model in make_models().items():
        model.fit(X_train, y_train)
        pred = np.maximum(model.predict(X_valid), 0)
        mae = float(mean_absolute_error(y_valid, pred))
        results.append(ModelResult(name=name, mae=mae, model=model))

    results.sort(key=lambda item: item.mae)
    return results, X_valid, y_valid


def train_final_model(best_name: str, X: pd.DataFrame, y: pd.Series) -> Pipeline:
    model = make_models()[best_name]
    model.fit(X, y)
    return model


def save_submission(model: Pipeline, X_test: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    pred = np.maximum(model.predict(X_test), 0)
    submission = pd.DataFrame({ID_COL: as_series(test[ID_COL]).astype(np.int64), PRICE_COL: pred})
    submission.to_csv(SUBMISSION_PATH, index=False)
    return submission


def save_charts(
    train: pd.DataFrame,
    feature_frame: pd.DataFrame,
    results: list[ModelResult],
    submission: pd.DataFrame,
) -> dict[str, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    charts: dict[str, Path] = {}

    price_dist = OUTPUT_DIR / "price_distribution.png"
    plt.figure(figsize=(8, 4.5), dpi=160)
    plt.hist(as_series(train[PRICE_COL]), bins=80, color="#2563eb", alpha=0.78)
    plt.title("训练集二手车价格分布")
    plt.xlabel("price")
    plt.ylabel("样本数量")
    plt.tight_layout()
    plt.savefig(price_dist)
    plt.close()
    charts["price_distribution"] = price_dist

    log_price_dist = OUTPUT_DIR / "log_price_distribution.png"
    plt.figure(figsize=(8, 4.5), dpi=160)
    plt.hist(np.log1p(as_series(train[PRICE_COL])), bins=80, color="#0f766e", alpha=0.78)
    plt.title("log1p(price) 后分布更平滑")
    plt.xlabel("log1p(price)")
    plt.ylabel("样本数量")
    plt.tight_layout()
    plt.savefig(log_price_dist)
    plt.close()
    charts["log_price_distribution"] = log_price_dist

    corr_path = OUTPUT_DIR / "top_correlations.png"
    corr_data = feature_frame.copy()
    corr_data[PRICE_COL] = as_series(train[PRICE_COL]).values
    corr = as_series(corr_data.corr(numeric_only=True)[PRICE_COL]).drop(PRICE_COL).abs().sort_values(ascending=False).head(12)
    plt.figure(figsize=(8, 4.8), dpi=160)
    corr.sort_values().plot(kind="barh", color="#dc2626")
    plt.title("与 price 相关性较高的特征")
    plt.xlabel("|相关系数|")
    plt.tight_layout()
    plt.savefig(corr_path)
    plt.close()
    charts["top_correlations"] = corr_path

    model_mae_path = OUTPUT_DIR / "model_mae.png"
    model_names = [r.name for r in results]
    maes = [r.mae for r in results]
    colors = ["#16a34a" if idx == 0 else "#64748b" for idx in range(len(maes))]
    plt.figure(figsize=(8, 4.5), dpi=160)
    bars = plt.bar(model_names, maes, color=colors)
    plt.title("验证集 MAE 对比（越低越好）")
    plt.ylabel("MAE")
    plt.xticks(rotation=12, ha="right")
    for bar, mae in zip(bars, maes):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{mae:.1f}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(model_mae_path)
    plt.close()
    charts["model_mae"] = model_mae_path

    pred_dist = OUTPUT_DIR / "prediction_distribution.png"
    plt.figure(figsize=(8, 4.5), dpi=160)
    plt.hist(as_series(submission[PRICE_COL]), bins=80, color="#7c3aed", alpha=0.78)
    plt.title("测试集预测价格分布")
    plt.xlabel("predicted price")
    plt.ylabel("样本数量")
    plt.tight_layout()
    plt.savefig(pred_dist)
    plt.close()
    charts["prediction_distribution"] = pred_dist

    return charts


def save_metrics(
    diagnostics: dict[str, int],
    results: list[ModelResult],
    submission: pd.DataFrame,
    X: pd.DataFrame,
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        **diagnostics,
        "feature_count": int(X.shape[1]),
        "best_model": results[0].name,
        "best_mae": results[0].mae,
        "models": [{"name": r.name, "mae": r.mae} for r in results],
        "submission_rows": int(len(submission)),
        "submission_min_price": float(as_series(submission[PRICE_COL]).min()),
        "submission_max_price": float(as_series(submission[PRICE_COL]).max()),
        "submission_mean_price": float(as_series(submission[PRICE_COL]).mean()),
    }
    METRICS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    train_raw, test_raw = load_data()
    train, diagnostics = clean_train(train_raw)
    test = clean_test(test_raw)
    X, X_test, y = prepare_features(train, test)
    results, _, _ = evaluate_models(X, y)
    final_model = train_final_model(results[0].name, X, y)
    submission = save_submission(final_model, X_test, test)
    charts = save_charts(train, X, results, submission)
    save_metrics(diagnostics, results, submission, X)

    print("二手车价格预测流程完成")
    print(f"最佳模型: {results[0].name}")
    print(f"验证集 MAE: {results[0].mae:.4f}")
    print(f"预测文件: {SUBMISSION_PATH}")
    print(f"指标文件: {METRICS_PATH}")


if __name__ == "__main__":
    main()
