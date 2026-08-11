import unittest

import pandas as pd

from api.air_quality import (
    classify_aqi,
    dominant_pollutant,
    linear_forecast,
    records_from_city_frames,
    summarize_dashboard,
)


class AirQualityTransformsTest(unittest.TestCase):
    def test_classify_aqi_uses_chinese_aqi_breakpoints(self):
        cases = [
            (50, "优"),
            (51, "良"),
            (150, "轻度污染"),
            (151, "中度污染"),
            (250, "重度污染"),
            (301, "严重污染"),
        ]

        for value, label in cases:
            with self.subTest(value=value):
                self.assertEqual(classify_aqi(value), label)

    def test_dominant_pollutant_uses_relative_standard_pressure(self):
        row = {
            "PM2.5": 52,
            "PM10": 80,
            "SO2": 10,
            "NO2": 35,
            "O3_8h": 80,
            "CO": 1.2,
        }

        self.assertEqual(dominant_pollutant(row), "PM2.5")

    def test_linear_forecast_extends_three_days_from_trend(self):
        forecast = linear_forecast([60, 62, 64, 66], horizon=3)

        self.assertEqual(forecast, [68.0, 70.0, 72.0])

    def test_records_from_city_frames_pivots_daily_pollutants(self):
        frame = pd.DataFrame(
            [
                {"date": 20260401, "hour": 1, "type": "AQI", "北京": 80, "上海": 60},
                {"date": 20260401, "hour": 2, "type": "AQI", "北京": 100, "上海": 70},
                {"date": 20260401, "hour": 1, "type": "PM2.5", "北京": 40, "上海": 20},
                {"date": 20260401, "hour": 2, "type": "PM2.5", "北京": 50, "上海": 30},
                {"date": 20260401, "hour": 1, "type": "PM10", "北京": 90, "上海": 50},
                {"date": 20260401, "hour": 1, "type": "SO2", "北京": 8, "上海": 6},
                {"date": 20260401, "hour": 1, "type": "NO2", "北京": 35, "上海": 25},
                {"date": 20260401, "hour": 1, "type": "O3_8h", "北京": 120, "上海": 80},
                {"date": 20260401, "hour": 1, "type": "CO", "北京": 1.0, "上海": 0.8},
            ]
        )

        records = records_from_city_frames([frame])

        beijing = next(item for item in records if item["city"] == "北京")
        self.assertEqual(beijing["date"], "2026-04-01")
        self.assertEqual(beijing["AQI"], 90.0)
        self.assertEqual(beijing["PM2.5"], 45.0)
        self.assertEqual(beijing["level"], "良")

    def test_summarize_dashboard_returns_required_sections(self):
        records = [
            {
                "date": "2026-04-01",
                "city": "北京",
                "AQI": 90.0,
                "PM2.5": 45.0,
                "PM10": 90.0,
                "SO2": 8.0,
                "NO2": 35.0,
                "O3_8h": 120.0,
                "CO": 1.0,
                "level": "良",
                "dominant": "PM2.5",
            },
            {
                "date": "2026-04-01",
                "city": "上海",
                "AQI": 65.0,
                "PM2.5": 25.0,
                "PM10": 55.0,
                "SO2": 6.0,
                "NO2": 28.0,
                "O3_8h": 86.0,
                "CO": 0.8,
                "level": "良",
                "dominant": "O3",
            },
        ]

        dashboard = summarize_dashboard(records, "2026-04-01", "2026-04-07")

        for key in [
            "summary",
            "mapPoints",
            "cityRank",
            "trend",
            "pollutantMix",
            "cityHeatmap",
            "levelDistribution",
        ]:
            self.assertIn(key, dashboard)
        self.assertEqual(dashboard["summary"]["dateRange"], "2026-04-01 至 2026-04-07")
        self.assertEqual(dashboard["summary"]["cityCount"], 2)
        self.assertEqual(dashboard["cityRank"]["cities"][0], "北京")


if __name__ == "__main__":
    unittest.main()
