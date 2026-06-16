#!/usr/bin/env python3
"""
全国空气质量可视化分析大屏 - Flask启动脚本
"""

import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api"))

from api.app import app  # noqa: E402


if __name__ == "__main__":
    print("=" * 64)
    print("  全国空气质量可视化分析大屏")
    print("=" * 64)
    print("  访问地址: http://127.0.0.1:5000")
    print("  数据周期: 2026-04-01 至 2026-04-07")
    print("  API:")
    print("    - GET /api/dashboard  - 获取完整大屏数据")
    print("    - GET /api/map        - 城市地图散点数据")
    print("    - GET /api/city-rank  - AQI城市排行")
    print("    - GET /api/trend      - 全国AQI趋势与预测")
    print("    - GET /api/pollutants - 污染物结构")
    print("    - GET /api/heatmap    - 城市日期热力图")
    print("    - GET /api/levels     - AQI等级分布")
    print("=" * 64)
    app.run(debug=True, host="0.0.0.0", port=5000)
