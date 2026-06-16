from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests


DATA_URL = "https://quotsoft.net/air/data/china_cities_{date}.csv"
POLLUTANTS = ["PM2.5", "PM10", "SO2", "NO2", "O3_8h", "CO"]
REQUIRED_TYPES = ["AQI", *POLLUTANTS]
DISPLAY_POLLUTANTS = {
    "PM2.5": "PM2.5",
    "PM10": "PM10",
    "SO2": "SO2",
    "NO2": "NO2",
    "O3_8h": "O3",
    "CO": "CO",
}
POLLUTANT_LIMITS = {
    "PM2.5": 75.0,
    "PM10": 150.0,
    "SO2": 150.0,
    "NO2": 80.0,
    "O3_8h": 160.0,
    "CO": 4.0,
}
LEVEL_ORDER = ["优", "良", "轻度污染", "中度污染", "重度污染", "严重污染"]
LEVEL_COLORS = {
    "优": "#2fbf71",
    "良": "#9ccf3b",
    "轻度污染": "#f3bf3b",
    "中度污染": "#f07f2f",
    "重度污染": "#dc4c64",
    "严重污染": "#7e3157",
}
CITY_COORDS = {
    "北京": [116.4074, 39.9042],
    "天津": [117.2000, 39.1333],
    "石家庄": [114.5149, 38.0428],
    "太原": [112.5492, 37.8706],
    "呼和浩特": [111.7492, 40.8426],
    "沈阳": [123.4315, 41.8057],
    "大连": [121.6147, 38.9140],
    "长春": [125.3235, 43.8171],
    "哈尔滨": [126.5349, 45.8038],
    "上海": [121.4737, 31.2304],
    "南京": [118.7969, 32.0603],
    "苏州": [120.5853, 31.2989],
    "无锡": [120.3119, 31.4912],
    "常州": [119.9741, 31.8112],
    "杭州": [120.1551, 30.2741],
    "宁波": [121.5504, 29.8746],
    "温州": [120.6994, 27.9949],
    "合肥": [117.2272, 31.8206],
    "芜湖": [118.4329, 31.3529],
    "福州": [119.2965, 26.0745],
    "厦门": [118.0894, 24.4798],
    "南昌": [115.8582, 28.6829],
    "赣州": [114.9348, 25.8311],
    "济南": [117.1201, 36.6512],
    "青岛": [120.3826, 36.0671],
    "烟台": [121.4479, 37.4638],
    "郑州": [113.6254, 34.7466],
    "洛阳": [112.4540, 34.6197],
    "武汉": [114.3055, 30.5928],
    "宜昌": [111.2865, 30.6919],
    "长沙": [112.9388, 28.2282],
    "株洲": [113.1517, 27.8358],
    "广州": [113.2644, 23.1291],
    "深圳": [114.0579, 22.5431],
    "珠海": [113.5767, 22.2707],
    "佛山": [113.1214, 23.0215],
    "东莞": [113.7518, 23.0207],
    "南宁": [108.3665, 22.8170],
    "桂林": [110.2900, 25.2736],
    "海口": [110.1983, 20.0442],
    "三亚": [109.5119, 18.2528],
    "重庆": [106.5516, 29.5630],
    "成都": [104.0665, 30.5723],
    "绵阳": [104.6791, 31.4675],
    "贵阳": [106.6302, 26.6470],
    "昆明": [102.8329, 24.8801],
    "拉萨": [91.1409, 29.6456],
    "西安": [108.9398, 34.3416],
    "兰州": [103.8343, 36.0611],
    "西宁": [101.7782, 36.6171],
    "银川": [106.2309, 38.4872],
    "石嘴山": [106.3833, 38.9832],
    "吴忠": [106.1984, 37.9976],
    "中卫": [105.1968, 37.5002],
    "乌鲁木齐": [87.6168, 43.8256],
    "和田地区": [79.9222, 37.1143],
    "喀什地区": [75.9898, 39.4704],
    "阿克苏地区": [80.2606, 41.1688],
    "克孜勒苏柯尔克孜自治州": [76.1678, 39.7145],
    "武威": [102.6380, 37.9282],
    "张掖": [100.4498, 38.9259],
    "西双版纳州": [100.7970, 22.0090],
    "吉林": [126.5494, 43.8378],
}


@dataclass(frozen=True)
class DateRange:
    start: str = "2026-04-01"
    end: str = "2026-04-07"

    def dates(self) -> list[str]:
        current = datetime.strptime(self.start, "%Y-%m-%d")
        end_date = datetime.strptime(self.end, "%Y-%m-%d")
        dates: list[str] = []
        while current <= end_date:
            dates.append(current.strftime("%Y%m%d"))
            current += timedelta(days=1)
        return dates


def classify_aqi(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "未知"
    if value <= 50:
        return "优"
    if value <= 100:
        return "良"
    if value <= 150:
        return "轻度污染"
    if value <= 200:
        return "中度污染"
    if value <= 300:
        return "重度污染"
    return "严重污染"


def dominant_pollutant(row: dict[str, float]) -> str:
    scores: dict[str, float] = {}
    for key, limit in POLLUTANT_LIMITS.items():
        value = row.get(key)
        if value is None or pd.isna(value):
            continue
        scores[key] = float(value) / limit
    if not scores:
        return "未知"
    pollutant = max(scores, key=scores.get)
    return DISPLAY_POLLUTANTS[pollutant]


def linear_forecast(values: list[float], horizon: int = 3) -> list[float]:
    if not values:
        return []
    if len(values) == 1:
        return [round(values[0], 1)] * horizon
    n = len(values)
    x_mean = (n - 1) / 2
    y_mean = sum(values) / n
    numerator = sum((i - x_mean) * (value - y_mean) for i, value in enumerate(values))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    slope = numerator / denominator if denominator else 0
    intercept = y_mean - slope * x_mean
    return [round(intercept + slope * (n + step), 1) for step in range(horizon)]


def download_city_csv(date: str, cache_dir: Path) -> pd.DataFrame:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"china_cities_{date}.csv"
    if cache_file.exists():
        return pd.read_csv(cache_file)

    response = requests.get(DATA_URL.format(date=date), timeout=30)
    response.raise_for_status()
    cache_file.write_bytes(response.content)
    return pd.read_csv(BytesIO(response.content))


def records_from_city_frames(frames: Iterable[pd.DataFrame]) -> list[dict[str, float | str]]:
    records: list[dict[str, float | str]] = []
    for frame in frames:
        working = frame[frame["type"].isin(REQUIRED_TYPES)].copy()
        city_columns = [column for column in working.columns if column not in {"date", "hour", "type"}]
        for date_value, day_frame in working.groupby("date"):
            date_label = datetime.strptime(str(int(date_value)), "%Y%m%d").strftime("%Y-%m-%d")
            for city in city_columns:
                if city.startswith("Unnamed"):
                    continue
                record: dict[str, float | str] = {"date": date_label, "city": city}
                for metric in REQUIRED_TYPES:
                    metric_values = pd.to_numeric(
                        day_frame.loc[day_frame["type"] == metric, city],
                        errors="coerce",
                    ).dropna()
                    if not metric_values.empty:
                        record[metric] = round(float(metric_values.mean()), 1)
                if "AQI" not in record:
                    continue
                record["level"] = classify_aqi(float(record["AQI"]))
                record["dominant"] = dominant_pollutant(record)  # type: ignore[arg-type]
                records.append(record)
    return records


def load_records(date_range: DateRange, cache_dir: Path) -> list[dict[str, float | str]]:
    frames = [download_city_csv(date, cache_dir) for date in date_range.dates()]
    return records_from_city_frames(frames)


def summarize_dashboard(
    records: list[dict[str, float | str]],
    start: str,
    end: str,
) -> dict[str, object]:
    if not records:
        raise ValueError("No air quality records available")

    city_values: defaultdict[str, list[float]] = defaultdict(list)
    city_pollutants: defaultdict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    date_values: defaultdict[str, list[float]] = defaultdict(list)
    city_day: defaultdict[str, dict[str, float]] = defaultdict(dict)
    level_counter: Counter[str] = Counter()
    dominant_counter: Counter[str] = Counter()

    for record in records:
        city = str(record["city"])
        date = str(record["date"])
        aqi = float(record["AQI"])
        city_values[city].append(aqi)
        date_values[date].append(aqi)
        city_day[city][date] = round(aqi, 1)
        level_counter[str(record.get("level", classify_aqi(aqi)))] += 1
        dominant_counter[str(record.get("dominant", "未知"))] += 1
        for pollutant in POLLUTANTS:
            value = record.get(pollutant)
            if value is not None and not pd.isna(value):
                city_pollutants[city][pollutant].append(float(value))

    city_avg = {
        city: round(sum(values) / len(values), 1)
        for city, values in city_values.items()
        if values
    }
    sorted_worst = sorted(city_avg.items(), key=lambda item: item[1], reverse=True)
    sorted_best = sorted(city_avg.items(), key=lambda item: item[1])
    all_aqi = [float(record["AQI"]) for record in records]
    dates = sorted(date_values)
    observed = [round(sum(date_values[date]) / len(date_values[date]), 1) for date in dates]
    forecast_dates = _next_dates(dates[-1], 3)
    forecast_values = linear_forecast(observed, 3)

    pollutant_mix = []
    for pollutant in POLLUTANTS:
        values = [
            float(record[pollutant])
            for record in records
            if pollutant in record and not pd.isna(record[pollutant])
        ]
        average = round(sum(values) / len(values), 1) if values else 0
        display_value = round(average * 100, 1) if pollutant == "CO" else average
        pollutant_mix.append(
            {
                "name": DISPLAY_POLLUTANTS[pollutant],
                "value": display_value,
                "rawValue": average,
                "unit": "mg/m3" if pollutant == "CO" else "ug/m3",
            }
        )

    heatmap_cities = [city for city, _ in sorted_worst[:8]]
    heatmap_values = []
    for city_index, city in enumerate(heatmap_cities):
        for date_index, date in enumerate(dates):
            heatmap_values.append([date_index, city_index, city_day[city].get(date, 0)])

    map_points = []
    for city, value in sorted_worst:
        coord = CITY_COORDS.get(city)
        if not coord:
            continue
        map_points.append(
            {
                "name": city,
                "value": [coord[0], coord[1], value],
                "aqi": value,
                "level": classify_aqi(value),
                "dominant": _average_dominant(city_pollutants[city]),
            }
        )

    max_city, max_aqi = sorted_worst[0]
    best_city, best_aqi = sorted_best[0]
    return {
        "summary": {
            "title": "全国空气质量可视化分析大屏",
            "dateRange": f"{start} 至 {end}",
            "cityCount": len(city_avg),
            "averageAqi": round(sum(all_aqi) / len(all_aqi), 1),
            "maxAqiCity": max_city,
            "maxAqi": max_aqi,
            "bestCity": best_city,
            "bestAqi": best_aqi,
            "dominantPollutant": dominant_counter.most_common(1)[0][0],
            "dataSource": "quotsoft 中国空气质量历史数据（原始来源：中国环境监测总站全国城市空气质量实时发布平台）",
            "reportSource": "生态环境部城市空气质量状况月报",
            "updateTime": "2026-04-08",
            "forecastNote": "预测值基于7日全国平均AQI线性趋势，仅作趋势演示。",
        },
        "mapPoints": map_points[:60],
        "cityRank": {
            "cities": [city for city, _ in sorted_worst[:8]],
            "values": [value for _, value in sorted_worst[:8]],
            "bestCities": [city for city, _ in sorted_best[:8]],
            "bestValues": [value for _, value in sorted_best[:8]],
        },
        "trend": {
            "dates": dates + forecast_dates,
            "observed": observed + [None] * len(forecast_values),
            "forecast": [None] * (len(observed) - 1) + [observed[-1]] + forecast_values,
        },
        "pollutantMix": pollutant_mix,
        "cityHeatmap": {
            "cities": heatmap_cities,
            "dates": [date[5:] for date in dates],
            "values": heatmap_values,
        },
        "levelDistribution": [
            {
                "name": level,
                "value": level_counter.get(level, 0),
                "color": LEVEL_COLORS[level],
            }
            for level in LEVEL_ORDER
        ],
        "conclusions": _build_conclusions(max_city, max_aqi, best_city, best_aqi, observed),
    }


def generate_dashboard(
    start: str = "2026-04-01",
    end: str = "2026-04-07",
    cache_dir: Path | None = None,
) -> dict[str, object]:
    date_range = DateRange(start, end)
    resolved_cache = cache_dir or Path(__file__).parent / "data" / "raw"
    records = load_records(date_range, resolved_cache)
    return summarize_dashboard(records, start, end)


def _next_dates(last_date: str, count: int) -> list[str]:
    current = datetime.strptime(last_date, "%Y-%m-%d")
    return [(current + timedelta(days=offset)).strftime("%Y-%m-%d") for offset in range(1, count + 1)]


def _average_dominant(values: dict[str, list[float]]) -> str:
    averages = {
        pollutant: sum(items) / len(items)
        for pollutant, items in values.items()
        if items
    }
    return dominant_pollutant(averages)


def _build_conclusions(
    max_city: str,
    max_aqi: float,
    best_city: str,
    best_aqi: float,
    observed: list[float],
) -> list[str]:
    direction = "上升" if observed[-1] > observed[0] else "下降"
    return [
        f"{max_city}为本周期AQI均值最高城市，平均AQI为{max_aqi}，需重点关注颗粒物与臭氧叠加影响。",
        f"{best_city}空气质量表现最好，平均AQI为{best_aqi}，整体处于较低污染水平。",
        f"全国平均AQI在7天内呈{direction}趋势，预测结果仅用于展示短期变化方向。",
    ]
