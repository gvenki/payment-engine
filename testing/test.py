import unittest
import sys
from collections import defaultdict
import logging


sys.path.append('../project')
from main_engine import deposit, Account, withdraw, dispute


class TestPaymentEngine(unittest.TestCase):
    def test_deposit_transaction(self):
        accounts = {1: Account(
            client=1,
            available=1
        )}
        deposit(accounts=accounts, client_id=1, amount=1.00)
        self.assertEqual(accounts[1].available, 2)

    def test_withdraw_transaction(self):
        accounts = defaultdict(Account)
        withdraw(accounts=accounts, client_id=1, amount=1.00)
        self.assertEqual(accounts[1].available, 0)

    def test_dispute_transaction(self):
        accounts = {1: Account(
            client=1,
            available=1
        )}
        dispute(accounts=accounts, client_id=1, amount=1.00, tx_id=22)
        self.assertEqual(accounts[1].available, 0)
        self.assertEqual(accounts[1].held, 1)
        self.assertEqual(accounts[1].held_txs, {22})
