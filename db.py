"""Database interface"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import model

class Database:
    """External database interface"""
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        model.Base.metadata.create_all(self.engine)

    def select_all_accounts(self):
        """Select all accounts sorted by registration date"""
        with Session(self.engine) as session:
            return session.query(model.Account).order_by(model.Account.created_at.desc()).all()

    def select_account(self, account_id):
        """Select an account by ID"""
        with Session(self.engine) as session:
            return session.query(model.Account).filter_by(account_id=account_id).first()

    def insert_accounts(self, account_list):
        """Create accounts from a list of names and emails"""
        with Session(self.engine) as session:
            for acc in account_list:
                account = session.query(model.Account).filter_by(account_name=acc['name']).first()
                if account is None:
                    session.add(model.Account(account_name=acc['name'], email=acc['email']))
            session.commit()
            return session.query(model.Account.account_id).filter(
                model.Account.account_name.in_([acc['name'] for acc in account_list])
            ).all()

    def update_account_name(self, account_id, account_name):
        """Change the name of an account"""
        with Session(self.engine) as session:
            session.query(model.Account).filter_by(account_id=account_id).update({
                'account_name': account_name
            })
            session.commit()

    def delete_accounts(self, account_id_list):
        """Delete accounts by ID"""
        with Session(self.engine) as session:
            deleted_accounts = []
            for account_id in account_id_list:
                account = self.select_account(account_id)
                if account is not None:
                    session.delete(account)
                    deleted_accounts.append(account_id)
            session.commit()
            return deleted_accounts
