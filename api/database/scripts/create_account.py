from api.database.main import create_session
from api.database.models.account import Account
from time import time
import json
from sqlalchemy.exc import IntegrityError

i_items = json.load(open('api/database/templates/i_items.json', 'r'))
i_locations = json.load(open('api/database/templates/i_locations.json', 'r'))

def create_account(steamID, country, username): 
    db_session = create_session()
    newAccount = Account(
        steamid=steamID,
        data={
            "reliclink": {
                "accountName": "/steam/" + str(steamID),
                "accountType": 3,
                "ssoID": -1,
                "ssoStatus": 0,
                "country": str(country),
                "currency": "usd",
                "spamAllowed": 2,
                "metaData": None
            },
            "profile_info": {
                "entityVersion": 517,
                "name": "/steam/" + str(steamID), 
                "metaData": "",
                "alias": str(username),
                "clanName": "",
                "xp": 0,
                "level": 1,
                "leaderboardRegionID": 0,
                "accountType": 3,
                "platformUserID": str(steamID),
                "linkedPlatformAccounts": []
            },
            "account_ban": {
                "level": 0,
                "message": "",
                "expiryDate": -1
            },
            "leaderboardStats": [
                {
                    "statGroupID": None,  
                    "leaderboardID": 0,
                    "wins": 0,
                    "losses": 0,
                    "streak": 0,
                    "disputes": 0,
                    "drops": 0,
                    "ranking": -1,
                    "rankTotal": -1,
                    "regionRanking": -1,
                    "regionRankTotal": -1,
                    "level": -1,
                    "rating": 0,
                    "counters": "{}",
                    "itemUseCount": "{}",
                    "lastMatchTime": int(time())
                }
            ],
            "stats": [
                {
                    "statID": 1,
                    "profileID": None, 
                    "value": 1,
                    "metadata": "",
                    "lastUpdated": int(time())
                } for i in range(1, 11)  
            ],
            "player_data": {
                "unknownNull": None,  
                "categoryIDs": [],
                "enableCrossplay": 1,
                "characterData": [[
                    None, 
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    int(time())
                ]],
                "privacySettings": [] 
            }
        },
        inventory=i_items,
        item_locations=i_locations
    )
    
    try:
        db_session.add(newAccount)
        db_session.commit()  
        
        data = newAccount.data
        data['player_data']['characterData'][0][0] = newAccount.id
        data['leaderboardStats'][0]['statGroupID'] = newAccount.id
        
        inventory = newAccount.inventory
        for i in inventory:
            i['profileID'] = newAccount.id
        
        for stat in data['stats']:
            stat['profileID'] = newAccount.id
            
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(newAccount, "data")
        flag_modified(newAccount, "inventory")
        
        db_session.commit()  
        
        #print(newAccount.id,
        #      newAccount.steamid,
        #      newAccount.data,
        #      newAccount.inventory,
        #      newAccount.item_locations)
        
        return newAccount.id
    except IntegrityError:
        db_session.rollback()
        raise
    finally:
        db_session.close()