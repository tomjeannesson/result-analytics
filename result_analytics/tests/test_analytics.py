import unittest

from result_analytics.src.analytics import Analytics


class TestAnalytics(unittest.TestCase):
    def test_aggregate_include(self):
        analytics = Analytics(sport="moguls")
        aggregated_df, all_df = analytics.aggregate(dimension="country", filters=[["M"], ["2023"], ["AH"], ["SF"]], filter_mode="include")
        self.assertTrue(len(all_df) == 1)

    def test_aggregate_exclude(self):
        analytics = Analytics(sport="moguls")
        aggregated_df, all_df = analytics.aggregate(dimension="athlete", filters=[["M", "F"], None, None, None], filter_mode="exclude")
        self.assertTrue(len(all_df) == 0)
