from api.database.main import create_session
from api.database.models.account import Account

session = create_session()

def get_userdata(account_id=None, steamid=None):
    if account_id != None:
        try:
            data = session.query(Account).filter_by(id=account_id).first()
            print(f'Requested userdata with account id user {account_id}')
            return data
        except ValueError as e:
            print(f"error {e}")
    if steamid != None:
        try:
            data = session.query(Account).filter_by(steamid=steamid).first()
            print(f'Requested userdata with steam id user {steamid}')
            return data
        except ValueError as e:
            print(f"error {e}")

        