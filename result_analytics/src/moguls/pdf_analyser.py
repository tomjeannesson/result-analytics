import contextlib
import os
from pathlib import Path

import pandas as pd
from PyPDF2 import PageObject, PdfReader

from result_analytics.src.moguls.athlete_result import MogulAthleteResult, Q2UselessDataFromFirstRun
from result_analytics.src.pdf_analyser import PdfAnalyser


class MogulPdfAnalyser(PdfAnalyser):
    def __init__(self) -> None:
        super().__init__()
        self.tree = self.tree["MO"]
        self.all_pdf = self.all_pdf_in_tree(self.tree)
        self.filters_shape = [None, None, None, None, None]

    @staticmethod
    def pdf_tree_sport(root_data: str) -> dict:
        tree = {}
        root_data = os.path.join(root_data, "MO")
        for circuit in os.listdir(root_data):
            tree[circuit] = {}
            for gender in os.listdir(os.path.join(root_data, circuit)):
                tree[circuit][gender] = {}
                for year in os.listdir(os.path.join(root_data, circuit, gender)):
                    tree[circuit][gender][year] = {}
                    for place in os.listdir(os.path.join(root_data, circuit, gender, year)):
                        tree[circuit][gender][year][place] = {}
                        for run in os.listdir(os.path.join(root_data, circuit, gender, year, place)):
                            if len(os.listdir(os.path.join(root_data, circuit, gender, year, place, run))) > 1:
                                error_msg = "Too many runs in folder. There should be only one run per folder."
                                raise ValueError(error_msg)
                            if len(os.listdir(os.path.join(root_data, circuit, gender, year, place, run))) == 0:
                                tree[circuit][gender][year][place][run] = None
                            else:
                                tree[circuit][gender][year][place][run] = os.listdir(os.path.join(root_data, circuit, gender, year, place, run))[0]
        return tree

    def analayse_pdf(self, pdf_name: list) -> dict:
        reader = PdfReader(os.path.join(Path(__file__).parent.parent.parent, "data", "MO", *pdf_name))
        all_athletes = {}
        for page in reader.pages:
            all_athletes = {**all_athletes, **self.analyse_page(page, pdf_name)}
        return all_athletes

    def analyse_page(self, page: PageObject, pdf_name: list) -> dict:
        text = page.extract_text()
        qualification = "QUALIFICATION" in text
        start_of_athlete_line = []
        for index, line in enumerate(text.split("\n")):
            if line.endswith("B:") and len(line.split(".")) <= 4:
                start_of_athlete_line.append(index)
            elif line.endswith("B:") and len(line.split(".")) == 8:
                start_of_athlete_line.append(index - 1)
        start_of_athlete_line.append(len(text.split("\n")))

        all_athletes = {}

        for i in range(len(start_of_athlete_line) - 1):
            athlete_line = "\n".join(text.split("\n")[start_of_athlete_line[i] : start_of_athlete_line[i + 1]])
            with contextlib.suppress(Q2UselessDataFromFirstRun):
                athlete = MogulAthleteResult(string=athlete_line, mode="qualification" if qualification else "final")
                all_athletes[f"{athlete.last_name} {athlete.first_name}"] = athlete
        return all_athletes

    def pdf_to_dataframe(self, pdf_name: list) -> dict:
        analysis = self.analayse_pdf(pdf_name)
        analysis = {athlete: analysis[athlete].to_dict() for athlete in analysis}
        return pd.DataFrame.from_dict(analysis, orient="index").sort_values(by="result")
