import unittest

from ledgerly._gen.rates_table import RATES


class TestRates(unittest.TestCase):
    def test_usd_eur(self):
        self.assertEqual(RATES[("USD", "EUR")], 0.9213)

    def test_every_pair(self):
        self.assertEqual(len(RATES), 30)
