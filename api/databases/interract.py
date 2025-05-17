from sqlalchemy.exc import IntegrityError
from time import time

from api.databases.db import *

def get_account_id(db_session, steamid=None):
    if steamid is not None:
        account = db_session.query(Account).filter_by(steamid=steamid).first()
        return account.id
    return None  

def get_account_data(db_session, account_id=None, steamid=None):
    if account_id is not None:
        account = db_session.query(Account).filter_by(id=account_id).first()
        return account.data
    elif steamid is not None:
        account = db_session.query(Account).filter_by(steamid=steamid).first()
        return account.data
    return None    

def create_account(db_session, steamID, country): 
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
        }
    )
    
    try:
        db_session.add(newAccount)
        db_session.commit()  
        
        data = newAccount.data
        data['player_data']['characterData'][0][0] = newAccount.id
        data['leaderboardStats'][0]['statGroupID'] = newAccount.id
        
        for stat in data['stats']:
            stat['profileID'] = newAccount.id
            
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(newAccount, "data")
        
        db_session.commit()  
        
        return newAccount.id
    except IntegrityError:
        db_session.rollback()
        raise
    finally:
        db_session.close()