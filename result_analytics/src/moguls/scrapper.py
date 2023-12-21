import contextlib
import os
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from result_analytics.src.scrapping import Scrapper


class MogulScrapper(Scrapper):
    def download(self, requested_path: Optional[str] = None, quick: bool = False) -> None:
        calendar_page = requests.get(self.full_url, timeout=5)
        soup = BeautifulSoup(calendar_page.content, "html.parser")
        soup = soup.find(id="calendardata")
        soup = soup.find_all("a")

        race_urls = {elem["href"] for elem in soup}
        all_downloads = []
        for url in race_urls:
            race_page = requests.get(url, timeout=5)
            soup = BeautifulSoup(race_page.content, "html.parser")
            place = soup.find(attrs={"class": "heading heading_l2 heading_off-sm-style heading_plain event-header__name"}).contents[0]
            year = self.seasoncode
            circuit = self.categorycode
            all_races_for_this_event = soup.find_all(attrs={"class": "clip"})
            for sport_div in all_races_for_this_event:
                for string in sport_div.contents:
                    if "Moguls" not in string:
                        continue
                    if "Dual" in string:
                        continue
                    if sport_div.parent.parent.parent.parent.parent.find_all(attrs={"class": "gender__item gender__item_m"}) != []:
                        gender = "M"
                    if sport_div.parent.parent.parent.parent.parent.find_all(attrs={"class": "gender__item gender__item_l"}) != []:
                        gender = "F"

                    all_downloads += [
                        ("MO", circuit, gender, year, place, div["href"])
                        for div in sport_div.parent.parent.parent.parent.parent.parent.parent.find_all(attrs={"name": "download"})
                        if div["href"].endswith(("RLF.pdf", "RLQ.pdf", "RLF1.pdf", "RLF2.pdf"))
                    ]
        all_downloads = set(all_downloads)
        for download in all_downloads:
            download = list(download)
            download[4] += f" - id: {download[-1].split('/')[-2]}"
            path = os.path.join(
                requested_path or Path(__file__).parent.parent.parent,
                "data",
                *download[:-1],
                download[-1].split("L")[-1].split(".")[0],
            )
            with contextlib.suppress(FileExistsError):
                os.makedirs(path)

            if not quick or os.listdir(path) == []:
                os.listdir(path)
                req = requests.get(download[-1], timeout=5)
                with open(
                    os.path.join(path, download[-1].split("/")[-1]),
                    "wb",
                ) as f:
                    f.write(req.content)
