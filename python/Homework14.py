from pathlib import Path

import pandas as pd
from pandas.api.types import is_string_dtype


def find_data_file() -> Path:
    """优先读取脚本同目录文件，找不到时读取下载目录中的附件。"""
    candidates = [
        Path(__file__).with_name("运动员信息表.csv"),
        Path.home() / "Downloads" / "运动员信息表.csv",
    ]

    for file_path in candidates:
        if file_path.exists():
            return file_path

    raise FileNotFoundError("未找到 运动员信息表.csv，请把文件放到脚本同目录或下载目录。")


def main() -> None:
    pd.set_option("display.unicode.east_asian_width", True)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

    data_file = find_data_file()
    athletes = pd.read_csv(data_file, encoding="gbk")

    # 去掉姓名、省份等文本列中多余的空格，避免筛选时漏掉数据。
    text_columns = [column for column in athletes.columns if is_string_dtype(athletes[column])]
    athletes[text_columns] = athletes[text_columns].apply(lambda col: col.str.strip())

    numeric_columns = ["年龄（岁）", "身高(cm)", "体重(kg)"]
    athletes[numeric_columns] = athletes[numeric_columns].apply(pd.to_numeric)

    print("原始数据前5行：")
    print(athletes.head())

    print("\n1）统计分析各个项目的运动员人数、平均身高、年龄、体重：")
    project_statistics = (
        athletes.groupby("项目")
        .agg(
            运动员人数=("姓名", "count"),
            平均身高=("身高(cm)", "mean"),
            平均年龄=("年龄（岁）", "mean"),
            平均体重=("体重(kg)", "mean"),
        )
        .round(2)
        .reset_index()
    )
    print(project_statistics)

    print("\n2）查询所有江西省女运动员的信息：")
    jiangxi_female = athletes[(athletes["省份"] == "江西省") & (athletes["性别"] == "女")]
    print(jiangxi_female)

    print("\n3）统计每个运动员的 BMI 值，并判断是否正常（正常区间：20~25）：")
    athletes["BMI"] = (athletes["体重(kg)"] / (athletes["身高(cm)"] / 100) ** 2).round(2)
    athletes["BMI是否正常"] = athletes["BMI"].between(20, 25, inclusive="both").map(
        {True: "正常", False: "不正常"}
    )

    bmi_result = athletes[
        ["姓名", "性别", "年龄（岁）", "身高(cm)", "体重(kg)", "项目", "省份", "BMI", "BMI是否正常"]
    ]
    print(bmi_result)


if __name__ == "__main__":
    main()
