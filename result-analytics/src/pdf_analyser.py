import os

from PyPDF2 import PageObject, PdfReader

from lib.athlete_result import AthleteResult


class PdfAnalyser:
    def analayse_pdf(self, pdf_name: str) -> dict:
        reader = PdfReader(f"data/{pdf_name}")
        all_athletes = {}
        for page in reader.pages:
            all_athletes = {**all_athletes, **self.analyse_page(page)}
        return all_athletes

    def analyse_page(self, page: PageObject) -> dict:
        text = page.extract_text()
        print(text)
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
            athlete = AthleteResult(string=athlete_line, qualification=qualification)
            all_athletes[f"{athlete.last_name} {athlete.first_name}"] = athlete
        return all_athletes


if __name__ == "__main__":
    for file_name in os.listdir("data"):
        analyser = PdfAnalyser()
        analyser.analayse_pdf(file_name)
    file_name = "taivalkoskiM.pdf"
    # file_name = "alpe.pdf"
    analyser = PdfAnalyser()
    res = analyser.analayse_pdf(file_name)
    # pprint(res)
