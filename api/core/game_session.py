from api.protocols.game.advertisement import host, updatePlatformLobbyID, update

from api.database.interract import get_userdata
from api.core.sessions import sessions_data

import json

values = json.load(open('data/values.json', 'r+'))
counters = values['counters']

cfg = json.load(open('config/config.json', 'r'))
cfg_b = cfg['battleserver']

def create_lobby(sessionID, hostid, relayRegion, party, race, team):
    counters['match_id'] +=1
    lobbyid = counters['match_id']
    
    result = host.advertisement_host(advertisementid=lobbyid,
                                     address=cfg_b['address'],
                                     ports=cfg_b['ports'],
                                     relayRegion=relayRegion,
                                     profileID=hostid,
                                     party=party,
                                     statGroupID=hostid, # using accountid value 
                                     raceID=race,
                                     team=team)
    print(f"User sid:{sessionID}|pid:{hostid} created new lobby with id {lobbyid}")
    
    global sessions_data
    user_session_data = sessions_data[f'{sessionID}']
    user_session_data['lobby_info'] = {
        "id": lobbyid,
        "platformLobbyID": None,
        "logged": True
    }
    return result

def update_session_PlatformLobbyID(sessionID, platformLobbyID):
    global sessions_data
    sessions_data[f'{sessionID}']['lobby_info']['platformLobbyID'] = platformLobbyID
    result = updatePlatformLobbyID.advertisements_updatePlatformLobbyID()
    print(sessions_data[f'{sessionID}'])
    return result

def update_lobby():
    result = update.advertisement_update()
    return result