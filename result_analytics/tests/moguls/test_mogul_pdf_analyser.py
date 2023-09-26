import unittest

from result_analytics.src.moguls.pdf_analyser import MogulPdfAnalyser

"""
python3 -m unittest result_analytics.tests.moguls.test_mogul_pdf_analyser -v
"""


class TestMogulPdfAnalyser(unittest.TestCase):
    def test_self_tree(self):
        tree = MogulPdfAnalyser().tree
        self.assertTrue(set(tree.keys()) == {"WC"})

    def test_analyse_pdf(self):
        analyser = MogulPdfAnalyser()
        for pdf_name in analyser.all_pdf:
            analyser.analayse_pdf(pdf_name)

    def test_pdf_to_dataframe(self):
        analyser = MogulPdfAnalyser()
        for pdf_name in analyser.all_pdf:
            analyser.pdf_to_dataframe(pdf_name)

    def test_analyse_specific_pdf(self):
        analyser = MogulPdfAnalyser()
        analyser.analayse_pdf(["WC", "M", "2023", "Alpe d'Huez (FRA) - id: 8787", "Q", "2023FS8787RLQ.pdf"])
