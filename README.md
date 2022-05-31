# payment-engine

## Overview
Implemented payment-engine using `python 3.9` using `pandas 1.3.4`, `collections`, and `unittest 1.1.0` modules

#### Folder structure
```
payment-engine/
|--engine/
    |--__init__.py
    |--main_engine.py
|--tests/
    |--__init__.py
    |--test.py
README.md
requirements.txt
```
## To Run
clone or download and unzip the repository and continue using any shell
```
cd payment-engine
pip install -r requirements.txt
python .\engine\main_engine.py  .\transactions.csv
```
`trasactions.csv` is a file with the columns type , client , tx , and amounta

To run the test cases 
```
cd tests
python -m unittest test.py
```

## Sample Outputs
```
################################ Final Account Overview ################################
client, available, held, total, locked
1, 1001.5, 0.0, 1001.5, False
2, 2.0, 0.0, 2.0, False
```

Output where account is locked

```
################################ Final Account Overview ################################
client, available, held, total, locked
1, 0.5, 0.0, 0.5, True
2, 2.0, 0.0, 2.0, False
```

#### For test cases
```
Ran 3 tests in 0.001s
OK
```
## Assumptions
These are the assumptions I made to complete the task
```
- python3 and pip are installed and available to execute
- Dispute occurs only after a sucessful withdrawl
- ChargeBack cannot happen to settled (Resolved) transactions
- Once the account is locked, all transactions including deposits are locked (ignored)
- If charge back occurs on 2nd trasaction after 5th transaction, account is locked but the transactions from 3 to 5 happen and are not voided
```
