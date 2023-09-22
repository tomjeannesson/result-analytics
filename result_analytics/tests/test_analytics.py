import unittest

from result_analytics.src.analytics import Analytics


class TestAnalytics(unittest.TestCase):
    def test_aggregate_include(self):
        analytics = Analytics(sport="moguls")
        aggregation = analytics.aggregate(dimension="athlete", filters=[["M"], ["2023"], ["AH"], ["Q"]], filter_mode="include")
        self.assertTrue(len(aggregation) == 1)

    def test_aggregate_exclude(self):
        analytics = Analytics(sport="moguls")
        aggregation = analytics.aggregate(dimension="athlete", filters=[["M", "F"], None, None, None], filter_mode="exclude")
        self.assertTrue(len(aggregation) == 0)
