from unittest import TestCase
import pandas as pd
from ID3.id3 import ID3


class TestID3(TestCase):

    def setUp(self) -> None:
        data_headers = ['engine', 'turbo', 'weight', 'fueleco', 'fast']
        self.data = pd.read_csv(
            "/home/john-gachihi/Downloads/A.I. exec code/id3_data.csv",
            names=data_headers,
            header=None
        )
        self.test_data = pd.read_csv(
            "/home/john-gachihi/Downloads/A.I. exec code/test_data.csv",
            names=data_headers,
            header=None
        )
        self.id3 = ID3(data_headers[:-1], data_headers[-1])
        self.expected_tree = {'fueleco': {'average': 'no', 'bad': {
            'weight': {'average': 'yes', 'heavy': {'engine': {'large': 'no', 'medium': {'turbo': {'no': 'no'}}}},
                       'light': {'turbo': {'no': 'no', 'yes': 'yes'}}}}, 'good': 'no'}}

    def test_generate_decision_tree(self):
        self.assertEqual(
            self.id3.generate_decision_tree(self.data),
            self.expected_tree
        )

    def test_classify(self):
        self.id3.generate_decision_tree(self.data)

        self.assertEqual(
            self.id3.classify(self.test_data),
            ['yes', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no']
        )

    def test_classify_when_decision_tree_is_empty(self):
        with self.assertRaises(Exception):
            self.id3.classify(self.test_data)