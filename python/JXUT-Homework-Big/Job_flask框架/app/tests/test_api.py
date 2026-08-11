import unittest

from api.app import app


class DashboardApiTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_dashboard_returns_air_quality_contract(self):
        response = self.client.get("/api/dashboard")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        for key in [
            "summary",
            "mapPoints",
            "cityRank",
            "trend",
            "pollutantMix",
            "cityHeatmap",
            "levelDistribution",
        ]:
            self.assertIn(key, payload)
        self.assertIn("空气质量", payload["summary"]["title"])
        self.assertIn(" 至 ", payload["summary"]["dateRange"])

    def test_refresh_returns_fixed_dashboard_without_random_drift(self):
        first = self.client.get("/api/refresh").get_json()
        second = self.client.get("/api/refresh").get_json()

        self.assertEqual(first["summary"]["averageAqi"], second["summary"]["averageAqi"])
        self.assertEqual(first["cityRank"], second["cityRank"])


if __name__ == "__main__":
    unittest.main()
