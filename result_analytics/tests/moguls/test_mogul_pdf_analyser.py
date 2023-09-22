import unittest

from result_analytics.src.moguls.pdf_analyser import MogulPdfAnalyser


class TestMogulPdfAnalyser(unittest.TestCase):
    def test_self_tree(self):
        tree = MogulPdfAnalyser().tree
        self.assertTrue(set(tree.keys()) == {"M", "F"})

    def test_analyse_pdf(self):
        analyser = MogulPdfAnalyser()
        for pdf_name in analyser.all_pdf:
            analyser.analayse_pdf(pdf_name)

    def test_pdf_to_dataframe(self):
        analyser = MogulPdfAnalyser()
        for pdf_name in analyser.all_pdf:
            analyser.pdf_to_dataframe(pdf_name)
