from __future__ import annotations

import html
import json
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager


ROOT = Path(__file__).resolve().parent
SOURCE_CSV = Path(
    r"C:\Users\y2003\Downloads\9--超市销售数据分析\9--超市销售数据分析\supermarket_1.csv"
)
DATA_DIR = ROOT / "data"
FIGURE_DIR = ROOT / "figures"
DATA_CSV = DATA_DIR / "supermarket_1.csv"
NOTEBOOK_PATH = ROOT / "超市销售数据分析报告-杨文天.ipynb"
HTML_PATH = ROOT / "超市销售数据分析报告-杨文天.html"
PDF_PATH = ROOT / "超市销售数据分析报告-杨文天.pdf"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def setup_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_CSV, DATA_CSV)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_CSV)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    for col in ["销售数量", "销售金额", "商品单价"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["销售日期_转换"] = pd.to_datetime(
        df["销售日期"].astype(str), format="%Y%m%d", errors="coerce"
    )
    df["销售月份_文本"] = df["销售月份"].astype(str).str[:4] + "-" + df["销售月份"].astype(str).str[4:]
    return df


def set_plot_style() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    font_path = Path(r"C:\Windows\Fonts\simhei.ttf")
    if not font_path.exists():
        font_path = Path(r"C:\Windows\Fonts\msyh.ttc")
    if font_path.exists():
        font_manager.fontManager.addfont(str(font_path))
        font_name = font_manager.FontProperties(fname=str(font_path)).get_name()
    else:
        font_name = "Microsoft YaHei"
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [font_name, "Microsoft YaHei", "SimHei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 140
    plt.rcParams["savefig.dpi"] = 160


def save_figures(df: pd.DataFrame) -> dict[str, Path]:
    set_plot_style()
    figures: dict[str, Path] = {}

    category_sales = (
        df.groupby("大类名称", as_index=True)["销售金额"].sum().sort_values(ascending=False)
    )
    top_category = category_sales.head(10).sort_values()
    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    bars = ax.barh(top_category.index, top_category.values, color="#3E7CB1")
    ax.set_title("各商品大类销售额 Top10")
    ax.set_xlabel("销售金额（元）")
    ax.bar_label(bars, labels=[f"{v:,.0f}" for v in top_category.values], padding=4, fontsize=8)
    fig.tight_layout()
    figures["category_top"] = FIGURE_DIR / "01_各商品大类销售额Top10.png"
    fig.savefig(str(figures["category_top"]), bbox_inches="tight")
    plt.close(fig)

    month_sales = df.groupby("销售月份_文本", as_index=True)["销售金额"].sum()
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    ax.plot(month_sales.index, month_sales.values, marker="o", linewidth=2.4, color="#C44536")
    ax.set_title("2015年1-4月销售额趋势")
    ax.set_xlabel("销售月份")
    ax.set_ylabel("销售金额（元）")
    for x, y in zip(month_sales.index, month_sales.values):
        ax.text(x, y, f"{y:,.0f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    figures["month_trend"] = FIGURE_DIR / "02_月度销售额趋势.png"
    fig.savefig(str(figures["month_trend"]), bbox_inches="tight")
    plt.close(fig)

    promo_stats = df.groupby("是否促销", as_index=True)[["销售金额", "销售数量"]].sum().loc[["否", "是"]]
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4))
    amount_bars = axes[0].bar(promo_stats.index, promo_stats["销售金额"], color=["#6C757D", "#F2A65A"])
    qty_bars = axes[1].bar(promo_stats.index, promo_stats["销售数量"], color=["#6C757D", "#F2A65A"])
    axes[0].set_title("促销与非促销销售额")
    axes[0].set_ylabel("销售金额（元）")
    axes[1].set_title("促销与非促销销售数量")
    axes[1].set_ylabel("销售数量")
    axes[0].bar_label(amount_bars, labels=[f"{v:,.0f}" for v in promo_stats["销售金额"]], padding=3, fontsize=8)
    axes[1].bar_label(qty_bars, labels=[f"{v:,.0f}" for v in promo_stats["销售数量"]], padding=3, fontsize=8)
    fig.suptitle("促销效果对比", y=1.02, fontsize=13)
    fig.tight_layout()
    figures["promo_compare"] = FIGURE_DIR / "03_促销效果对比.png"
    fig.savefig(str(figures["promo_compare"]), bbox_inches="tight")
    plt.close(fig)

    type_sales = df.groupby("商品类型", as_index=True)["销售金额"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    colors = ["#4D908E", "#F9C74F", "#577590"]
    ax.pie(
        type_sales.values,
        labels=type_sales.index,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        colors=colors[: len(type_sales)],
    )
    ax.set_title("不同商品类型销售额占比")
    fig.tight_layout()
    figures["type_share"] = FIGURE_DIR / "04_商品类型销售额占比.png"
    fig.savefig(str(figures["type_share"]), bbox_inches="tight")
    plt.close(fig)

    return figures


def fmt_money(value: float) -> str:
    return f"{value:,.2f}"


def build_summary(df: pd.DataFrame) -> dict[str, object]:
    category_sales = df.groupby("大类名称")["销售金额"].sum().sort_values(ascending=False)
    month_sales = df.groupby("销售月份_文本")["销售金额"].sum()
    promo_sales = df.groupby("是否促销")["销售金额"].sum().sort_values(ascending=False)
    type_sales = df.groupby("商品类型")["销售金额"].sum().sort_values(ascending=False)
    return {
        "row_count": len(df),
        "col_count": 18,
        "clean_col_count": len(df.columns),
        "total_amount": df["销售金额"].sum(),
        "total_qty": df["销售数量"].sum(),
        "customers": df["顾客编号"].nunique(),
        "items": df["商品编码"].nunique(),
        "invalid_dates": int(df["销售日期_转换"].isna().sum()),
        "month_min": month_sales.index.min(),
        "month_max": month_sales.index.max(),
        "best_month": month_sales.idxmax(),
        "best_month_amount": month_sales.max(),
        "weak_month": month_sales.idxmin(),
        "weak_month_amount": month_sales.min(),
        "top_categories": category_sales.head(5),
        "promo_amount": promo_sales.get("是", 0.0),
        "no_promo_amount": promo_sales.get("否", 0.0),
        "type_sales": type_sales,
    }


def md_lines(text: str) -> list[str]:
    lines = text.strip("\n").splitlines()
    return [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines else [])


def code_lines(text: str) -> list[str]:
    lines = text.strip("\n").splitlines()
    return [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines else [])


def markdown_cell(text: str) -> dict[str, object]:
    return {"cell_type": "markdown", "metadata": {}, "source": md_lines(text)}


def code_cell(text: str) -> dict[str, object]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code_lines(text),
    }


def figure_md(path: Path, title: str, conclusion: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return f"#### {title}\n\n![{title}]({rel})\n\n{conclusion}"


def make_report_markdown(summary: dict[str, object], figures: dict[str, Path]) -> list[dict[str, object]]:
    top_categories: pd.Series = summary["top_categories"]  # type: ignore[assignment]
    type_sales: pd.Series = summary["type_sales"]  # type: ignore[assignment]
    top_text = "、".join(f"{name}（{fmt_money(value)}元）" for name, value in top_categories.items())
    total_amount = float(summary["total_amount"])
    promo_amount = float(summary["promo_amount"])
    promo_rate = promo_amount / total_amount * 100
    first_type = type_sales.index[0]
    first_type_rate = type_sales.iloc[0] / total_amount * 100

    cells = [
        markdown_cell(
            """
# 超市销售数据分析报告

学生姓名：杨文天
"""
        ),
        markdown_cell(
            f"""
### 一、需求分析

本项目基于超市 2015 年 1 月至 4 月的销售明细数据，目的是从销售规模、品类结构、月份变化和促销效果等角度发现经营特点，为门店备货、促销安排和品类优化提供数据支持。

- 分析维度 1：总体经营情况。统计销售金额、销售数量、顾客数、商品数等核心指标，判断数据规模和经营基础。
- 分析维度 2：商品大类销售结构。使用各商品大类销售额 Top 图，找出贡献最高的核心品类。
- 分析维度 3：月份销售趋势。使用月度销售额折线图，观察 2015 年 1-4 月销售额的波动情况。
- 分析维度 4：促销效果与商品类型结构。使用促销对比图和商品类型占比图，分析促销销售贡献和商品类型构成。
"""
        ),
        markdown_cell(
            f"""
### 二、结论

本次数据共 {summary["row_count"]} 条销售记录，覆盖 {summary["customers"]} 位顾客、{summary["items"]} 个商品，统计期内总销售额为 {fmt_money(total_amount)} 元，总销售数量为 {float(summary["total_qty"]):,.2f}。

- 重点品类集中明显。销售额最高的前五个大类为：{top_text}。其中日配、蔬果、休闲和粮油是主要销售来源，后续备货和陈列应优先保障这些高贡献品类。
- 月份销售存在波动。{summary["best_month"]} 销售额最高，为 {fmt_money(float(summary["best_month_amount"]))} 元；{summary["weak_month"]} 销售额最低，为 {fmt_money(float(summary["weak_month_amount"]))} 元。说明门店销售并非平均分布，应结合节假日、促销和季节变化提前安排库存。
- 促销商品销售额为 {fmt_money(promo_amount)} 元，占总销售额约 {promo_rate:.1f}%。促销有一定带动作用，但非促销销售仍是主要收入来源，促销应重点用于拉动高潜力品类，而不是简单扩大范围。
- 商品类型中，{first_type} 销售贡献最高，占总销售额约 {first_type_rate:.1f}%。一般商品是稳定收入基础，生鲜类则适合通过新鲜度、陈列和组合促销提升复购。
"""
        ),
        markdown_cell(
            """
### 三、过程和思考

下面按照“数据读取与预处理、描述统计、可视化分析、分析结论”的流程展开。代码保留完整计算过程，图表后给出对应分析说明。
"""
        ),
        code_cell(
            """
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
"""
        ),
        code_cell(
            """
data_path = "data/supermarket_1.csv"
df = pd.read_csv(data_path)

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

for col in ["销售数量", "销售金额", "商品单价"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["销售日期_转换"] = pd.to_datetime(
    df["销售日期"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)
df["销售月份_文本"] = df["销售月份"].astype(str).str[:4] + "-" + df["销售月份"].astype(str).str[4:]

df.head()
"""
        ),
        code_cell(
            """
basic_info = {
    "记录数": len(df),
    "字段数": df.shape[1],
    "顾客数": df["顾客编号"].nunique(),
    "商品数": df["商品编码"].nunique(),
    "总销售数量": df["销售数量"].sum(),
    "总销售金额": df["销售金额"].sum(),
    "日期转换异常数": df["销售日期_转换"].isna().sum()
}
basic_info
"""
        ),
        markdown_cell(
            f"""
#### 1：数据读取、描述分析与预处理

读取数据后删除原 CSV 中多余的 `Unnamed: 0` 索引列，并将销售数量、销售金额、商品单价转为数值类型。销售日期按 `%Y%m%d` 转换，其中 `20150229` 不是合法日期，转换异常共 {summary["invalid_dates"]} 条；这些记录数量很少，因此保留原始销售月份字段继续做月度分析。
"""
        ),
        code_cell(
            """
category_sales = df.groupby("大类名称")["销售金额"].sum().sort_values(ascending=False)
category_sales.head(10)
"""
        ),
        markdown_cell(
            figure_md(
                figures["category_top"],
                "2.1 商品大类销售额分析",
                "从图中可以看出，销售额主要集中在日配、蔬果、休闲、粮油、酒饮等大类。门店应优先保证这些高贡献品类的库存稳定，同时结合货架位置和促销活动提升购买转化。",
            )
        ),
        code_cell(
            """
month_sales = df.groupby("销售月份_文本")["销售金额"].sum()
month_sales
"""
        ),
        markdown_cell(
            figure_md(
                figures["month_trend"],
                "2.2 月度销售趋势分析",
                f"从 2015 年 1-4 月看，{summary['best_month']} 销售额最高，{summary['weak_month']} 销售额最低。销售波动说明门店运营需要按月份提前做备货计划，并关注节假日、季节和促销安排对销售的影响。",
            )
        ),
        code_cell(
            """
promo_stats = df.groupby("是否促销")[["销售金额", "销售数量"]].sum()
promo_stats
"""
        ),
        markdown_cell(
            figure_md(
                figures["promo_compare"],
                "2.3 促销效果分析",
                f"促销销售额占总销售额约 {promo_rate:.1f}%，说明促销对销售有贡献，但非促销销售仍占主导。后续可把促销资源集中到高毛利、高复购或需要清库存的商品，避免促销投入过于分散。",
            )
        ),
        code_cell(
            """
type_sales = df.groupby("商品类型")["销售金额"].sum().sort_values(ascending=False)
type_sales
"""
        ),
        markdown_cell(
            figure_md(
                figures["type_share"],
                "2.4 商品类型结构分析",
                f"商品类型中，{first_type} 的销售额占比最高，是门店收入的主要基础。生鲜类销售额也有明显贡献，应重视保鲜、损耗控制和日常陈列；联营商品占比较低，可结合场地和利润贡献评估是否优化。",
            )
        ),
        markdown_cell(
            """
### 四、过程反思

本次分析先从数据清洗入手，再围绕销售额、品类、月份和促销四个维度进行可视化。分析过程中发现，日期字段存在少量非法日期，因此实际分析时不能盲目直接转换日期，而要先检查异常值。通过图表可以更直观地看到核心销售来源和月份波动，后续如果继续深入，可以增加客单价、复购情况、单品贡献和促销前后对比等分析，使经营建议更加细化。
"""
        ),
    ]
    return cells


def write_notebook(cells: list[dict[str, object]]) -> None:
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
                "file_extension": ".py",
                "mimetype": "text/x-python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")


def markdown_to_html(text: str) -> str:
    lines = text.strip("\n").splitlines()
    out: list[str] = []
    in_list = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append(f"<p>{html.escape(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_paragraph()
            close_list()
            continue
        if line.startswith("![") and "](" in line and line.endswith(")"):
            flush_paragraph()
            close_list()
            alt = line[2 : line.index("]")]
            src = line[line.index("(") + 1 : -1]
            out.append(f'<img src="{html.escape(src)}" alt="{html.escape(alt)}">')
        elif line.startswith("#### "):
            flush_paragraph()
            close_list()
            out.append(f"<h4>{html.escape(line[5:])}</h4>")
        elif line.startswith("### "):
            flush_paragraph()
            close_list()
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("# "):
            flush_paragraph()
            close_list()
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("- "):
            flush_paragraph()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{html.escape(line[2:])}</li>")
        else:
            paragraph.append(line)
    flush_paragraph()
    close_list()
    return "\n".join(out)


def write_html(cells: list[dict[str, object]]) -> None:
    body_parts: list[str] = []
    for cell in cells:
        source = "".join(cell["source"])  # type: ignore[index]
        if cell["cell_type"] == "markdown":
            body_parts.append(markdown_to_html(source))
        else:
            body_parts.append(f"<pre><code>{html.escape(source)}</code></pre>")

    css = """
body {
  font-family: "Microsoft YaHei", "SimHei", Arial, sans-serif;
  color: #172033;
  line-height: 1.7;
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 40px;
}
h1 { text-align: center; font-size: 30px; margin-bottom: 8px; }
h3 { border-left: 6px solid #315f8f; padding-left: 10px; margin-top: 28px; }
h4 { margin-top: 24px; color: #25496f; }
img { display: block; max-width: 92%; margin: 12px auto 18px; }
pre {
  white-space: pre-wrap;
  background: #f5f7fa;
  border: 1px solid #d8dee8;
  border-radius: 6px;
  padding: 12px 14px;
  font-size: 12px;
  line-height: 1.45;
}
ul { padding-left: 24px; }
@page { size: A4; margin: 16mm 14mm; }
"""
    html_text = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(body_parts)}</body></html>"
    HTML_PATH.write_text(html_text, encoding="utf-8")


def write_pdf() -> None:
    if not CHROME.exists():
        raise FileNotFoundError(f"Chrome not found: {CHROME}")
    subprocess.run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            f"--print-to-pdf={PDF_PATH}",
            str(HTML_PATH),
        ],
        check=True,
    )


def verify_outputs(df: pd.DataFrame) -> None:
    assert df.shape[0] == 42726
    assert abs(float(df["销售金额"].sum()) - 454210.62) < 0.01
    assert abs(float(df["销售数量"].sum()) - 51256.56) < 0.01
    assert df["顾客编号"].nunique() == 2612
    assert df["商品编码"].nunique() == 6138
    assert df["销售月份"].min() == 201501
    assert df["销售月份"].max() == 201504
    for path in [DATA_CSV, NOTEBOOK_PATH, HTML_PATH, PDF_PATH]:
        assert path.exists() and path.stat().st_size > 0, path
    assert len(list(FIGURE_DIR.glob("*.png"))) >= 4
    parsed = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    assert parsed["nbformat"] == 4
    notebook_text = NOTEBOOK_PATH.read_text(encoding="utf-8")
    for phrase in ["需求分析", "结论", "过程和思考"]:
        assert phrase in notebook_text


def main() -> None:
    setup_dirs()
    df = load_data()
    figures = save_figures(df)
    summary = build_summary(df)
    cells = make_report_markdown(summary, figures)
    write_notebook(cells)
    write_html(cells)
    write_pdf()
    verify_outputs(df)
    print("OK")
    print(f"notebook={NOTEBOOK_PATH}")
    print(f"pdf={PDF_PATH}")
    print(f"figures={FIGURE_DIR}")


if __name__ == "__main__":
    main()
