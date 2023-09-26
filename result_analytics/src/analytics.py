from typing import Optional

from result_analytics.src.moguls import MogulPdfAnalyser

ANALYSERS = {"MO": MogulPdfAnalyser}


class Analytics:
    def __init__(self, sport: str) -> None:
        self.analyser = ANALYSERS[sport]()

    def aggregate(self, dimension: str, filters: Optional[list] = None, filter_mode: str = "exclude"):
        filters = filters or self.analyser.filters_shape

        if len(filters) != len(self.analyser.filters_shape):
            error_msg = f"Filters shape should be of length {len(self.analyser.filters_shape)}."
            raise ValueError(error_msg)

        if dimension not in ["athlete", "country"]:
            error_msg = f"Dimension {dimension} not supported. Supported dimensions are athlete and country."
            raise ValueError(error_msg)

        if filter_mode not in ["exclude", "include"]:
            error_msg = f"Filter mode {filter_mode} not supported. Supported filter modes are exclude and include."
            raise ValueError(error_msg)

        aggregated_df = {}
        all_df = []
        for pdf_name in self.analyser.all_pdf:
            valid = True
            if filter_mode == "exclude":
                for index, filter_list in enumerate(filters):
                    if filter_list is None:
                        continue
                    for tag in filter_list:
                        if tag == pdf_name[index]:
                            valid = False
                            break
                    if not valid:
                        break
            elif filter_mode == "include":
                for index, tag in enumerate(pdf_name[:-1]):  # the [:-1] is to exclude the pdf name
                    if filters[index] is None:
                        continue
                    if tag not in filters[index]:
                        valid = False
                        break
            if valid:
                analysis = self.analyser.pdf_to_dataframe(pdf_name)
                if dimension == "athlete":
                    for athlete_name in analysis.index:
                        aggregated_df[athlete_name] = [*aggregated_df.get(athlete_name, []), analysis]
                elif dimension == "country":
                    for country_name in analysis["country"].unique():
                        aggregated_df[country_name] = [*aggregated_df.get(country_name, []), analysis]
                all_df.append(analysis)
        return aggregated_df, all_df
