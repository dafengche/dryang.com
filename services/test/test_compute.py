import unittest

from compute import compute

class TestCompute(unittest.TestCase):

    def setUp(self):
        pass

    def test_add(self):
        self.assertEqual(compute.add(1, 2), 3)

    def test_sub(self):
        self.assertEqual(compute.sub(1, 2), -1)

    def test_mul(self):
        self.assertEqual(compute.mul(2, 3), 6)

    def test_div(self):
        self.assertEqual(compute.div(6, 2), 3)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
