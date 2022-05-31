import pandas as pd
from collections import defaultdict


class Account:
    def __init__(self, client=None, available=0.0, held=0.0, held_txs=None, total=0.0, locked=False):
        if held_txs is None:
            held_txs = set()
        self.client = client
        self.available = available
        self.held = held
        self.held_txs = held_txs
        self.total = total
        self.locked = locked

    def __str__(self):
        return "client: %s, available: %s, held: %s, total: %s, locked: %s" % (self.client, self.available,
                                                                               self.held, self.total,
                                                                               self.locked)


def deposit(accounts: dict, client_id: int, amount: float):
    accounts[client_id].available += float(amount)
    accounts[client_id].total = accounts[client_id].available + accounts[client_id].held


def withdraw(accounts: dict, client_id: int, amount: float):
    if accounts[client_id].available > float(amount):
        accounts[client_id].available -= float(amount)
    else:
        pass
        # print("Withdrawal Failed for client : %s for amount: %s " % (client_id, amount))
    accounts[client_id].total = accounts[client_id].available + accounts[client_id].held


def dispute(accounts: dict, client_id: int, amount: float, tx_id: int):
    accounts[client_id].available -= amount
    accounts[client_id].held += amount
    accounts[client_id].held_txs.add(tx_id)


def resolve(accounts: dict, client_id: int, amount: float, tx_id: int):
    if tx_id in accounts[client_id].held_txs:
        accounts[client_id].held_txs.remove(tx_id)
        accounts[client_id].available += amount
        accounts[client_id].held -= amount


def charge_back(accounts: dict, client_id: int, amount: float, tx_id: int):
    if tx_id in accounts[client_id].held_txs:
        accounts[client_id].held_txs.remove(tx_id)
        accounts[client_id].total -= amount
        accounts[client_id].held -= amount
        accounts[client_id].locked = True


def get_matching_tx(tx_df: pd.DataFrame, tx_id: int):
    return tx_df[(tx_df['tx'] == tx_id) & (tx_df['type'] != "dispute")
                                         & (tx_df['type'] != "resolve")]


def calculate_balance(accounts: dict, tx_df: pd.DataFrame, each_user: int):
    accounts[each_user].client = each_user  # setting client ID

    for each_transaction in tx_df.itertuples():
        client_id = getattr(each_transaction, 'client')
        tx_id = getattr(each_transaction, 'tx')
        type_of_tx = getattr(each_transaction, 'type')
        amount = getattr(each_transaction, 'amount')

        if accounts[client_id].locked:
            continue
        if type_of_tx == 'deposit':
            deposit(accounts, client_id, amount)

        elif type_of_tx == 'withdrawal':
            withdraw(accounts, client_id, amount)

        elif type_of_tx == 'dispute':
            matching_transaction = get_matching_tx(tx_df, tx_id)
            if len(matching_transaction):
                dispute(accounts, client_id, matching_transaction.iloc[0].amount, tx_id)

        elif type_of_tx == 'resolve':
            matching_transaction = get_matching_tx(tx_df, tx_id)
            if len(matching_transaction):
                resolve(accounts, client_id, matching_transaction.iloc[0].amount,  tx_id)
        else:
            matching_transaction = get_matching_tx(tx_df, tx_id)
            if len(matching_transaction):
                charge_back(accounts, client_id, matching_transaction.iloc[0].amount, tx_id)


def main():
    accounts = defaultdict(Account)
    transactions = pd.read_csv(r'../transactions.csv', sep=r',', skipinitialspace=True)
    for each_user in set(transactions['client']):
        calculate_balance(accounts, transactions.loc[transactions['client'] == each_user], each_user)
    print('''################################ Final Account Overview ################################''')
    for key, value in accounts.items():
        print(value)


if __name__ == "__main__":
    main()
