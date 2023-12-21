import unittest
from pprint import pprint

from result_analytics.src.analytics import Analytics

"""
python3 -m unittest result_analytics.tests.test_analytics -v
"""


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

    def test_aggregate_specific(self):
        analytics = Analytics(sport="MO")
        dimension = "athlete"
        aggregated_df, all_df = analytics.aggregate(
            dimension=dimension,
            # filters=[None, ["M"], None, None, None],
            filters=[["WC"], ["M"], ["2023"], ["Alpe d'Huez (FRA) - id: 8159"], ["F", "F1"]],
            filter_mode="include",
        )
        print()
        extract = analytics.extract(aggregated_dataframes=aggregated_df, dimension=dimension, dimension_value="HORISHIMA Ikuma")
        pprint(extract)
