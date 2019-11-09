from unittest import TestCase
from ID3.decision_tree import DecisionTree


class TestDecisionTree(TestCase):

    def test_add_to_tree_when_path_is_empty(self):
        dt = DecisionTree()
        dt.add_to_tree([], 'a', True)

        self.assertEqual(dt.get_tree(), {'a': dict()})

    def test_add_to_tree_when_adding_decision_node(self):
        dt = DecisionTree(tree={'a': {'b': {'c': dict()}}})
        dt.add_to_tree([('a', 'b'), ('c', 'd')], 'e')

        self.assertEqual(dt.get_tree(), {'a': {'b': {'c': {'d': 'e'}}}})

    def test_add_to_tree_when_adding_tree_root(self):
        dt = DecisionTree(tree={'a': {'b': {'c': dict()}}})
        dt.add_to_tree([('a', 'b'), ('c', 'd')], 'e', True)

        self.assertEqual(dt.get_tree(), {'a': {'b': {'c': {'d': {'e': dict()}}}}})