from api.protocols.game.account.getProfileName import *
from api.protocols.game.Leaderboard.getStatGroupsByProfileIDs import Leaderboard_getStatGroupsByProfileIDs
from api.protocols.game.account.FindProfilesByPlatformID import account_FindProfilesByPlatformID
from api.protocols.game.relationship.getRelationships import relationship_getRelationships

from api.database import interract
from api.core.sessions import sessions_data, clients_list

from api.utils.datautils import relicjson

def data_getProfileName(profile_ids):
    for id in profile_ids:
        account_data = interract.get_userdata(account_id=id)
        banState = account_data.data['account_ban']['expiryDate']
        if banState == -1:
            ban = None
        data = getProfileName(u_profile=account_data.data['profile_info'],
                              id=account_data.id,
                              banInfo=ban)
        return relicjson(data)

def data_getStatGroupsByProfileIDs(ids, sessionID):
    session_data = sessions_data[f'{sessionID}']
    account_data = interract.get_userdata(account_id=ids[1])
    banState = account_data.data['account_ban']['expiryDate']
    if banState == -1:
        ban = None
    
    data = Leaderboard_getStatGroupsByProfileIDs(id=ids[1],
                                                 profile_info=account_data.data['profile_info'],
                                                 name=session_data['username'],
                                                 u_leaderboardStats=account_data.data['leaderboardStats'],
                                                 banState=ban)
    return data

def players_FindProfilesByPlatformID(platformIDs):
    pids = list(platformIDs)  
    target_profiles = []
    
    for item in pids:
        for client in clients_list:  
            if isinstance(client, dict) and 'platformUserID' in client: 
                if client['platformUserID'] == item:  
                    target_profiles.append(item)
                    print(f"{item}")  

    result = account_FindProfilesByPlatformID(target_profiles)  
    
    return result

def data_getRelationships(sessionID):
    result = relationship_getRelationships(
        relationships="[],[],[],[],[],[],[]"
    )
    return result