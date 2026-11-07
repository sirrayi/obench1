import unittest
from unittest import mock

from harbor.billing import late_fees

MOCK = {"id": 1, "name": "mocked", "tier": "team", "deleted": False}


class TestLateFees(unittest.TestCase):
    def test_owner_mocked(self):
        with mock.patch("harbor.accounts.fetch_user", return_value=MOCK):
            self.assertEqual(late_fees.late_fee_payer(3), "late_fee_payer:mocked:team:0")

    def test_population(self):
        self.assertEqual(late_fees.late_fee_population(), 4242)
