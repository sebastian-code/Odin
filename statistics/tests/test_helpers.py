from unittest import TestCase

from helpers import division_or_zero


class HelpersTest(TestCase):
    def test_division(self):
        self.assertAlmostEqual(1.66666666667, division_or_zero(5, 3), places=7)

    def test_division_by_zero(self):
        self.assertEqual(0, division_or_zero(5, 0))
