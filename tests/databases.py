from api.databases.db import *
from api.databases.interract import *

db_session = create_session()        
        
steamID = "76561198617872072"
country = "ru"

account_id = create_account(db_session=db_session, steamID=steamID, country=country)
print(f"Created account with ID: {account_id}")

print(f'the account id is: {get_account_id(db_session=db_session, steamid=int(steamID))}')
print(f'the account data is: {get_account_data(db_session=db_session, steamid=int(steamID))}')
