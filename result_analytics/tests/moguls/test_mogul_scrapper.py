import unittest

from result_analytics.src.moguls.scrapper import MogulScrapper

"""
python3 -m unittest result_analytics.tests.moguls.test_mogul_scrapper -v
"""


class TestMogulScrapper(unittest.TestCase):
    def test_download(self):
        scrapper = MogulScrapper(
            base_url="https://www.fis-ski.com/DB/freestyle-freeski/ski-cross/calendar-results.html",
            url_kwargs={
                "eventselection": "results",
                "place": "",
                "sectorcode": "FS",
                "seasoncode": "2023",
                "categorycode": "WC",
                "disciplinecode": "MO",
                "gendercode": "",
                "racedate": "",
                "racecodex": "",
                "nationcode": "",
                "seasonmonth": "X-2023",
                "saveselection": "1",
                "seasonselection": "#download-white",
            },
        )

        scrapper.download(requested_path="./result_analytics/")
        scrapper = MogulScrapper(
            base_url="https://www.fis-ski.com/DB/freestyle-freeski/ski-cross/calendar-results.html",
            url_kwargs={
                "eventselection": "results",
                "place": "",
                "sectorcode": "FS",
                "seasoncode": "2022",
                "categorycode": "WC",
                "disciplinecode": "MO",
                "gendercode": "",
                "racedate": "",
                "racecodex": "",
                "nationcode": "",
                "seasonmonth": "X-2023",
                "saveselection": "1",
                "seasonselection": "#download-white",
            },
        )

        scrapper.download()
