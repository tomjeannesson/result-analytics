import statistics
from typing import Optional

import numpy as np

from result_analytics.src.moguls import MogulPdfAnalyser

ANALYSERS = {"MO": MogulPdfAnalyser}


class Analytics:
    def __init__(self, sport: str, requested_path: Optional[str] = None) -> None:
        self.analyser = ANALYSERS[sport](requested_path=requested_path)

    def aggregate(self, dimension: str, filters: Optional[list] = None, filter_mode: str = "exclude"):
        """Filter should be a list of list of strings.

        The first is the circuit, the second is the genre, the third is the year, the fourth is the place, the fifth is the run type.
        Example: ["WC"], ["M"], ["2023"], ["Alpe d'Huez (FRA) - id: 8159"], ["F"]
        """
        filters = filters or self.analyser.filters_shape

        if len(filters) != len(self.analyser.filters_shape):
            error_msg = f"Filters shape should be of length {len(self.analyser.filters_shape)}."
            raise ValueError(error_msg)

        if dimension not in ["athlete", "country", "top_air", "bottom_air"]:
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
                elif dimension == "top_air":
                    for top_air in analysis["top_air_trick"].unique():
                        aggregated_df[top_air] = [*aggregated_df.get(top_air, []), analysis]
                elif dimension == "bottom_air":
                    for bottom_air in analysis["bottom_air_trick"].unique():
                        aggregated_df[bottom_air] = [*aggregated_df.get(bottom_air, []), analysis]
                all_df.append(analysis)
        return aggregated_df, all_df

    def generate_stats(self, data: list):
        quantiles = statistics.quantiles(data, n=4)
        return {
            "raw": data,
            "avg": quantiles[1],
            "std": statistics.stdev(data),
            "q1": quantiles[0],
            "q3": quantiles[2],
        }

    def extract(self, aggregated_dataframes: dict, dimension: str, dimension_value: str):
        stats = {}
        for dataframe in aggregated_dataframes[dimension_value]:
            if dimension == "country":
                dataframe = dataframe.set_index("country")
            if dimension == "top_air":
                dataframe = dataframe.set_index("top_air_trick")
            if dimension == "bottom_air":
                dataframe = dataframe.set_index("bottom_air_trick")
            dataframe["ski_judge_base"] = (
                dataframe["ski_judge1"] + dataframe["ski_judge2"] + dataframe["ski_judge3"] + dataframe["ski_judge4"] + dataframe["ski_judge5"]
            ) / 5
            dataframe["ski_judge_deductions"] = (
                dataframe["ski_deduction_judge1"]
                + dataframe["ski_deduction_judge2"]
                + dataframe["ski_deduction_judge3"]
                + dataframe["ski_deduction_judge4"]
                + dataframe["ski_deduction_judge5"]
            ) / 5
            dataframe["top_air"] = (dataframe["top_air_judge1"] + dataframe["top_air_judge2"]) / 2
            dataframe["bottom_air"] = (dataframe["bottom_air_judge1"] + dataframe["bottom_air_judge2"]) / 2
            for column in dataframe.columns:
                data = dataframe[column][dimension_value]
                if isinstance(data, (str, int, float, np.int64, np.float64)):
                    data = [data]
                for elem in data:
                    if column == "time":
                        rank = np.nan if isinstance(elem, str) else len(dataframe[dataframe[column] < elem]) + 1
                    else:
                        rank = np.nan if isinstance(elem, str) else len(dataframe[dataframe[column] > elem]) + 1
                    stats[column] = {
                        "raw": [*stats.get(column, {"raw": []})["raw"], elem],
                        "rank": [*stats.get(column, {"rank": []})["rank"], rank],
                    }

        cleaned_up_stats = {}

        match dimension:
            case "athlete":
                for stat in [
                    "air_points",
                    "time_points",
                    "ski_points",
                    "total_points",
                    "ski_deduction_total",
                    "ski_deduction_total",
                    "ski_judge_deductions",
                    "ski_judge_base",
                    "top_air",
                    "bottom_air",
                ]:
                    cleaned_up_stats[stat] = {
                        "raw": self.generate_stats(stats[stat]["raw"]),
                        "rank": self.generate_stats(stats[stat]["rank"]),
                    }

                cleaned_up_stats["top_air"]["coeff"] = self.generate_stats(stats["top_air_coefficient"]["raw"])
                cleaned_up_stats["bottom_air"]["coeff"] = self.generate_stats(stats["bottom_air_coefficient"]["raw"])
                cleaned_up_stats["ski_judge_base"]["total"] = self.generate_stats(stats["ski_total"]["raw"])
                cleaned_up_stats["ski_judge_deductions"]["total"] = self.generate_stats(stats["ski_deduction_total"]["raw"])
            case _:
                raise NotImplementedError

        return cleaned_up_stats
