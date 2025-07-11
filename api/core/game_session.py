from api.protocols.game.advertisement import host, update, updatePlatformLobbyID, leave, peerAdd, updateState

from api.core.sessions import sessions_data
from api.core.matchmaking import lobbies_json, create_lobby

import json
import zlib
import base64
from hexdump import hexdump

values = json.load(open('data/values.json', 'r+'))
counters = values['counters']

cfg = json.load(open('config/config.json', 'r'))
cfg_b = cfg['battleserver']

def init_game_session(sessionID, hostid, visible, mapname, options, slotinfo, maxplayers, matchType, relayRegion, party, race, team, isObservable, observerDelay, passworded):
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
        "isHost": True,
        "MatchStarted": False,
        "logged": True,
    }
    
    create_lobby(matchID=lobbyid,
                 hostID=hostid,
                 visible=visible,
                 mapname=mapname,
                 options=options,
                 slotinfo=slotinfo,
                 passworded=passworded,
                 maxplayers=maxplayers,
                 matchType=matchType,
                 relayRegion=relayRegion,
                 isObservable=isObservable,
                 observerDelay=observerDelay)
    
    return result

def update_session_PlatformLobbyID(sessionID, lobby_id, platformLobbyID):
    global lobbies_json
    for lobby in lobbies_json:
        if lobby["id"] == int(lobby_id):
            lobby['platformlobbyid'] = int(platformLobbyID)
            print(json.dumps(lobby, indent=4))
    global sessions_data
    sessions_data[f'{sessionID}']['lobby_info']['platformLobbyID'] = platformLobbyID
    result = updatePlatformLobbyID.advertisements_updatePlatformLobbyID()
    print(json.dumps(sessions_data[f'{sessionID}'], indent=4))
    return result

def update_lobby(advertisementid=int,
                 description=str,
                 mapname=str,
                 isObservable=int,
                 matchType=int,
                 maxplayers=int,
                 observerDelay=int,
                 options=str,
                 passworded=int,
                 slotinfo=str,
                 state=int,
                 visible=int):
    global lobbies_json
    
    print(f"[GameSession] updating {advertisementid}")
    print(f"description: {description}")
    print(f"mapname: {mapname}")
    print(f"matchType: {matchType}")
    print(f"maxplayers: {maxplayers}")
    print(f"options: {options}")
    print(f"slotInfo: {slotinfo}")
    print(f"state: {state}")
    print(f"observable: {isObservable}")
    print(f"observerDelay: {observerDelay}")
    
    #print('==================================================')
    #print(f'Decoded "options" field:')
    #hexdump(zlib.decompress(base64.b64decode(options)))
    #print(f'Decoded "slotinfo"field :')
    #print(f'{zlib.decompress(base64.b64decode(slotinfo))}')
    #print('==================================================')
    
    for lobby in lobbies_json:
        if lobby["id"] == advertisementid:
            lobby["mapname"] = mapname
            lobby["matchType"] = matchType
            lobby["maxplayers"] = maxplayers
            lobby["options"] = options
            lobby["passworded"] = passworded
            lobby["slotinfo"] = slotinfo
            lobby["state"] = state
            if lobby["state"] == 1:
                lobby["state"] = 1
            lobby["isObservable"] = isObservable
            lobby["observerDelay"] = observerDelay,
            if lobby['observerDelay'] is not int:
                lobby['observerDelay'] = 180
            lobby["visible"] = visible
        #print(json.dumps(lobby, indent=4))
    print(json.dumps(lobbies_json))

def updateState(advertisementid,
                state):
    for lobby in lobbies_json:
        if lobby['id'] == advertisementid:
            lobby['state'] = state
        for peer in lobby['peers']:
            p_session = sessions_data[f'{peer['profileID']}']
            p_session['lobby_info']['MatchStarted'] = True

# party operations
def add_peer(profile_ids, raceIDs, teamIDs, match_id=int): # adding new peer to the party (lobby)
    global lobbies_json
    
    print(f"Adding peers to lobby {match_id}: profiles={profile_ids}, races={raceIDs}, teams={teamIDs}")
    
    print(lobbies_json)
    
    lobby_found = False
    for lobby in lobbies_json:
        print(f"Checking lobby id: {lobby['id']}")      
        if lobby["id"] == match_id:
            lobby_found = True
            if len(profile_ids) != len(raceIDs) or len(raceIDs) != len(teamIDs):
                print("Error: Lengths of profile_ids, raceIDs, and teamIDs do not match.")
                return
            
            for profile_id, race_id, team_id in zip(profile_ids, raceIDs, teamIDs):
                peer = {
                    "advertisementID": match_id,
                    "profileID": profile_id,
                    "party": -1,
                    "statGroupID": profile_id,
                    "raceID": race_id,
                    "team": team_id,
                    "route": "/10.0.7.136" 
                }
                lobby["peers"].append(peer)
                print(f"Added peer: {json.dumps(peer, indent=2)}")
            
            print(f"Updated lobby: {json.dumps(lobby, indent=2)}")
            break
    
    if not lobby_found:
        print(f"Lobby with id {match_id} not found.")


def peer_leave(sessionID, advertisementID):  # handling peer leave from lobby
    global lobbies_json
    global sessions_data
    session = sessions_data.get(f'{sessionID}') 
    if not session:
        print(f"[Error] Session {sessionID} not found.")
        return

    peer_profileID = session['account']
    
    if 'lobby_info' in session:  
        del session['lobby_info']  
    
    for lobby in lobbies_json:
        if lobby["id"] == advertisementID:
            # removing host peer
            if lobby['hostid'] == peer_profileID:
                peers = [peer for peer in lobby['peers'] if peer["profileID"] != lobby['hostid']]
                if peers:  # Check if there are any peers left
                    lobby['hostid'] = peers[0]["profileID"]
                else:
                    print(f"[GameSession] No peers left in lobby {advertisementID}.")
            
            # delete lobby if no peers in it
            if not lobby['peers']:
                print(f"[GameSession] Removing lobby {advertisementID} due to emptiness.")
                lobbies_json = [lobby for lobby in lobbies_json if lobby["id"] != advertisementID]
                print(f"[GameSession] Lobby {advertisementID} removed. Current lobbies: {lobbies_json}")
                return  
    
    result = leave.advertisement_leave()  # response
    return result


def update_Host(sessionID, advertisementID):
    global lobbies_json
    global sessions_data
    session = sessions_data[f'{sessionID}'] 
    for lobby in lobbies_json:
        if lobby['id'] == advertisementID:
            peers = len(lobby['peers'])
            result = f'[{peers[0]}]'
            
            session['lobby_info']['isHost'] = True
            print(f'[GameSession] Host changed in lobby {advertisementID}, new host is pID {peers[0]['profileID']}')
            
            return result