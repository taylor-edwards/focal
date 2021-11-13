import sys
from db import Database
from time import sleep

db = Database('postgresql+psycopg2://focal:asdf@127.0.0.1:5432/focal')

account_list = [ \
    { 'name': 'chumpy', 'email': 'chumpy@focal.pics' }, \
    { 'name': 'skeletor', 'email': 'skeletor@focal.pics' }, \
]
print(f"Added accounts {db.insert_accounts(account_list)}")

sleep(1)

account_list = [ \
    { 'name': 'nacho', 'email': 'nacho@focal.pics' }, \
    { 'name': 'jojo', 'email': 'jojo@focal.pics' } \
]
print(f"Added accounts {db.insert_accounts(account_list)}")

db.update_account_name(102, 'cheese')

print(f"Renaming account 102: {db.select_account(102).account_name}")

print(f"Deleting accounts: {db.delete_accounts([103])}")

print("All accounts: " + ', '.join([ \
    f'{account.account_name} ({account.account_id})' for account in db.select_all_accounts() \
]))

if __name__ == '__main__':
  sys.exit(0)
