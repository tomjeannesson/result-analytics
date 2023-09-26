import unittest

from result_analytics.src.analytics import Analytics


class TestAnalytics(unittest.TestCase):
    def test_aggregate_include(self):
        analytics = Analytics(sport="MO")
        aggregated_df, all_df = analytics.aggregate(
            dimension="country",
            filters=[["WC"], ["M"], ["2023"], ["Alpe d'Huez (FRA) - id: 8159"], ["F"]],
            filter_mode="include",
        )
        self.assertTrue(len(all_df) == 1)

    def test_aggregate_exclude(self):
        analytics = Analytics(sport="MO")
        aggregated_df, all_df = analytics.aggregate(dimension="athlete", filters=[None, ["M", "F"], None, None, None], filter_mode="exclude")
        self.assertTrue(len(all_df) == 0)
