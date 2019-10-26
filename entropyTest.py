import unittest
from math import log2

# from decision_tree_id3 import entropy


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_entropy(self):
        expected = (-(10/15)*log2(10/15) - ((5/15)*log2(5/15))) - ((11/15)*(-((8/11)*log2(8/11)) -((3/11)*log2(3/11)))  +  (4/15)*(-(2/4)*log2(2/4)-(2/4)*log2(2/4)))
        actual = 0.03170514719803619
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
