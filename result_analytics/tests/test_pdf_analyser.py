import unittest

from result_analytics.src.pdf_analyser import PdfAnalyser


class TestPdfAnalyser(unittest.TestCase):
    def test_tree_sports(self):
        tree = PdfAnalyser().pdf_tree()
        self.assertTrue(set(tree.keys()) == {"MO"})

    def test_tree_genders(self):
        tree = PdfAnalyser().pdf_tree()
        for circuit_dict in tree.values():
            for sport, genders_dict in circuit_dict.items():
                self.assertTrue(set(genders_dict.keys()) == {"M", "F"}, f"Sport: {sport} missing genders. ({list(genders_dict.keys())})")

    def test_tree_years(self):
        tree = PdfAnalyser().pdf_tree()

        for circuit_dict in tree.values():
            for genders_dict in circuit_dict.values():
                for gender, year_dict in genders_dict.items():
                    self.assertTrue(set(year_dict.keys()) == {"2022", "2023"}, f"Gender: {gender} missing years. ({list(year_dict.keys())})")

    def test_all_pdf_in_tree(self):
        PdfAnalyser().pdf_tree()

    def test_all_pdf_in_specific_tree_1(self):
        all_pdf = PdfAnalyser.all_pdf_in_tree(
            {
                "moguls": {
                    "F": {
                        "2022": {"AH": {"F": None, "Q": None, "SF": None}, "DV": {"F": None, "Q": None, "SF": None}},
                        "2023": {"AH": {"F": None, "Q": None, "SF": "2023FS8160RLF.pdf"}, "DV": {"F": None, "Q": None, "SF": None}},
                    },
                    "M": {
                        "2022": {"AH": {"F": None, "Q": None, "SF": None}, "DV": {"F": None, "Q": None, "SF": None}},
                        "2023": {
                            "AH": {"F": "2023FS8159RLF1.pdf", "Q": "2023FS8787RLQ.pdf", "SF": "2023FS8159RLF.pdf"},
                            "DV": {"F": None, "Q": None, "SF": None},
                        },
                    },
                },
            },
        )
        self.assertEqual(len(all_pdf), 4)

    def test_all_pdf_in_specific_tree_2(self):
        all_pdf = PdfAnalyser.all_pdf_in_tree(
            {
                "F": {
                    "2022": {"AH": {"F": None, "Q": None, "SF": None}, "DV": {"F": None, "Q": None, "SF": None}},
                    "2023": {"AH": {"F": None, "Q": None, "SF": "2023FS8160RLF.pdf"}, "DV": {"F": None, "Q": None, "SF": None}},
                },
                "M": {
                    "2022": {"AH": {"F": None, "Q": None, "SF": None}, "DV": {"F": None, "Q": None, "SF": None}},
                    "2023": {
                        "AH": {"F": "2023FS8159RLF1.pdf", "Q": "2023FS8787RLQ.pdf", "SF": "2023FS8159RLF.pdf"},
                        "DV": {"F": None, "Q": None, "SF": None},
                    },
                },
            },
        )
        self.assertEqual(len(all_pdf), 4)
