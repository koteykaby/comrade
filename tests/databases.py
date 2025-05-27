from api.database.scripts import create_account
from api.database.interract import get_userdata
        
steamID = "76561198617872072"
country = "ru"

account_id = create_account(steamID=steamID, country=country)
print(f"Created account with ID: {account_id}")
print(f'the account data is: {get_userdata(steamid=int(steamID))}')
