from api.models.advertisement import Peer, Lobby
from api.utils.datautils import relicjson
from api.protocols.game.advertisement.findAdvertisements import advertisement_findAdvertisements
from api.protocols.game.advertisement.getAdvertisements import advertisement_getAdvertisements
from api.protocols.game.advertisement.join import advertisements_join
import json
from api.core.sessions import sessions_data

global lobbies_json
lobbies_json = []  

cfg = json.load(open('config/config.json'))
cfg_b = cfg['battleserver']

def create_lobby(matchID=int,
                 hostID=int, 
                 visible=int,
                 mapname=str, 
                 options=str,
                 passworded=int, 
                 slotinfo=str, 
                 maxplayers=int, 
                 matchType=int, 
                 relayRegion=str,
                 isObservable=int,
                 observerDelay=int):
    lobby_data = {
        "id": matchID,
        "platformlobbyid": None,
        "unk": "0",
        "hostid": hostID,
        "state": 0,
        "description": "SESSION_MATCH_KEY",
        "visible": visible,
        "mapname": mapname,
        "options": options,
        "passworded": passworded,
        "maxplayers": maxplayers,
        "slotinfo": slotinfo,
        "matchType": matchType,
        "peers": [],
        "unk2": 0,
        "unk3": 512,
        "isObservable": isObservable,
        "observerDelay": observerDelay,
        "unk4": 0,
        "unk5": 0,
        "startGameTime": None,
        "relayRegion": relayRegion,
        "endGameTime": None
    }    
    global lobbies_json
    lobbies_json.append(lobby_data)
    
    print("[Matchmaking] Created new lobby!")
    print(f"ID: {lobby_data['id']}")
    print(f"Map: {lobby_data['mapname']}")
    print(f"Options: {lobby_data['options']}")
    print(f"SlotInfo: {lobby_data['slotinfo']}")
    print(f"MatchType: {lobby_data['matchType']}")
    print(f"RelayRegion: {lobby_data['relayRegion']}")
    
def make_lobbies_list() -> list[Lobby]:
    global lobbies_json
    lobbies_copy = lobbies_json.copy()
    result_list = []
    for lobby_d in lobbies_copy:
        target_lobby = lobby_d.copy()
        peers_l = [Peer(**peer) for peer in target_lobby['peers']]
        target_lobby.pop('peers')
        result = Lobby(
            **target_lobby,
            peers=peers_l
        )
        result_list.append(result)
    return result_list

def discover():
    lobbies = make_lobbies_list()
    data = advertisement_findAdvertisements(lobbies)
    return data

def get_advertisements(matchIDs):
    global lobbies_json
    result = [] 
    for lobby in lobbies_json:
        lobby_d = lobby.copy()
        for match in matchIDs:
            if lobby['id'] == int(match):  
                peers_l = [Peer(**peer) for peer in lobby_d.pop('peers', [])]  
                advs = [Lobby(
                    **lobby_d,
                    peers=peers_l
                )]
                advertisement = advertisement_getAdvertisements(advs=advs)
                result.append(advertisement) 
    return result

def remove_lobby(peer_profileID):
    # delete lobby from list if host peer is gone and no one is exist in it
    lobbies_json = [lobby for lobby in lobbies_json if lobby["hostid"] != peer_profileID and len(lobby['peers']) == []]

def join_lobby(sessionID, advID, party, raceID, teamID):
    global lobbies_json
    global sessions_data
    
    session = sessions_data[f'{sessionID}']
    platform_lobby_id = next((lobby['platformLobbyID'] for lobby in lobbies_json if lobby['id'] == advID), None)
    
    session['lobby_info'] = {
        "id": advID,
        "platformLobbyID": platform_lobby_id,
        "isHost": False,
        "MatchStarted": False
    }
    
    result = advertisements_join(address=cfg_b['address'],
                                 ports=cfg_b['ports'],
                                 advid=advID,
                                 p_id=sessions_data[f'{sessionID}']['account'],
                                 party=party,
                                 r_id=raceID,
                                 t_id=teamID)
    return result