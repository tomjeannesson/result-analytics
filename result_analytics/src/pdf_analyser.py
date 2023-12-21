import os
from typing import Optional


class PdfAnalyser:
    def __init__(self, requested_path: Optional[str] = None) -> None:
        self.tree = self.pdf_tree(requested_path=requested_path)
        self.all_pdf = self.all_pdf_in_tree(self.tree)

    def pdf_tree(self, requested_path: Optional[str] = None) -> dict:
        tree = {}
        root_data = requested_path or os.path.join("result_analytics", "data")
        for sport in os.listdir(root_data):
            tree[sport] = PdfAnalyser.pdf_tree_sport(root_data, sport)
        return tree

    @staticmethod
    def all_pdf_in_tree(tree: dict, name: Optional[list] = None) -> list:
        prefix = name or []
        all_pdf = []
        for key, value in tree.items():
            if isinstance(value, str):
                all_pdf.append([*prefix, key, value])
            if isinstance(value, dict):
                values = PdfAnalyser.all_pdf_in_tree(tree=value, name=[*prefix, key])
                all_pdf += values
        return all_pdf

    @staticmethod
    def pdf_tree_sport(root_data, sport):
        if sport == "MO":
            from result_analytics.src.moguls.pdf_analyser import MogulPdfAnalyser

            return MogulPdfAnalyser.pdf_tree_sport(root_data=root_data)
        error_msg = f"Sport {sport} not supported. Supported sports are moguls."
        raise ValueError(error_msg)
