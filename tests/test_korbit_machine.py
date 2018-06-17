import unittest
from machine.korbit_machine import KorbitMachine
import inspect

class KorbitMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.korbit_machine = KorbitMachine()
        self.notest_set_token()

    def tearDown(self):
        pass

    def notest_set_token(self):
        print(inspect.stack()[0][3])
        expire, access_token, refresh_token = self.korbit_machine.set_token(grant_type="password")
        assert access_token
        print("Expire:", expire, "Access_token:", access_token, "Refresh_token:", refresh_token)

    def notest_get_token(self):
        print(inspect.stack()[0][3])
        self.korbit_machine.set_token(grant_type="password")
        access_token = self.korbit_machine.get_token()
        assert access_token
        print(access_token)

    def notest_get_ticker(self):
        print(inspect.stack()[0][3])
        ticker = self.korbit_machine.get_ticker("etc_krw")
        assert ticker
        print(ticker)

    def notest_get_filled_orders(self):
        print(inspect.stack()[0][3])
        order_book = self.korbit_machine.get_filled_orders(currency_type="btc_krw")
        assert order_book
        print(order_book)

    def test_get_wallet_status(self):
        print(inspect.stack()[0][3])
        wallet_status = self.korbit_machine.get_wallet_status()
        assert wallet_status
        print(wallet_status)

if __name__ == "__main__":
    unittest.main()