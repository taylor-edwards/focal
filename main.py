import sys
from db2 import Database

db = Database('postgresql+psycopg2://albumator@127.0.0.1:5432/albumator')
db.bootstrap()
users = db.select_all_users()
print(users)
# db.insert_users(['jojo'])
# users = db.select_all_users()
# print(users)
# db.delete_users(['jojo'])
# users = db.select_all_users()
# print(users)

if __name__ == '__main__':
  sys.exit(0)
