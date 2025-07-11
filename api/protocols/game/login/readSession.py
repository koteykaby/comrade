from dataclasses import dataclass
from api.protocols.game.login.structures import PresenceProfile, PlatformSessionUpdateMessage, MatchStartMessage
from api.models.advertisement import Lobby
from typing import List
from time import time
from api.utils.datautils import relicjson

@dataclass
class PresenceMessageStruct:
    unk: int
    description: str
    profileid: int
    data: any
    
def do_EmptyRead():
    return [[]]

def do_PresenceMessage(profileid,
                       u_profile,
                       banInfo):        
    result = [[PresenceMessageStruct(
        unk=0,
        description="PresenceMessage",
        profileid=profileid,
        data=[PresenceProfile(
            **u_profile,
            id=profileid,
            personalStatGroupID=profileid,
            banInfo=banInfo,
            presenceID=1,
            presenceLocalized=None,
            presencePropertyInfo=[]
        )
        ]
    )]]
    return result

def do_PlatformSessionUpdateMessage_ReadSessionMessage(profileid,
                                                       lobbyid,
                                                       platformlobbyid):
    result = [[PlatformSessionUpdateMessage(
        status_code=0,
        description="PlatformSessionUpdateMessage",
        host_id=profileid,
        lobby_ids=[
            lobbyid,
            "0",
            platformlobbyid
        ]
    )]]
    return result

@dataclass
class PeerInventoryItem:
    profile_id: str
    items: any
    
@dataclass
class MatchStartMessage:
    status_code: int
    description: str
    profile_id: int
    unk_peer_data: any
    start_game_time: int
    peers_inventory: List[PeerInventoryItem] 
    current_match_info: Lobby 
    unknown_peer_data: List[List] 

def do_MatchStartMessage(profileID, current_lobby):
    current_lobby['startGameTime'] = int(time())
    
    lobby_data = current_lobby.copy()
    
    converted_peers = [
        [
            peer['advertisementID'],
            peer['profileID'],
            peer['party'],
            peer['statGroupID'],
            peer['raceID'],
            peer['team'],
            peer['route']
        ] for peer in current_lobby['peers']
    ]
    
    lobby_data['peers'] = converted_peers
    
    peers_data = []
    peer_ids = []
    peers_inventory = []
    unknown_peer_data = []
    
    for i, peer in enumerate(current_lobby['peers']):
        # unkown peer data (i don't know what these values means, but it must be the same)
        peers_data.append([
            peer['profileID'],
            [231430, 231451, 317850]  
        ])
        
        peer_ids.append([
            str(peer['profileID']),
            str(i) 
        ])
        
        peers_inventory.append([
            str(peer['profileID']),
            []
        ])

        unknown_peer_data.append([
            str(peer['profileID']),
            []
        ])
    
    result = [[
        MatchStartMessage(
            status_code=0,
            description="MatchStartMessage",
            profile_id=int(profileID),
            unk_peer_data=[peers_data, peer_ids],
            start_game_time=int(time()),
            peers_inventory=peers_inventory,
            current_match_info=Lobby(**lobby_data),
            unknown_peer_data=unknown_peer_data
        )
    ]]
    
    return result

#print(relicjson(do_MatchStartMessage(profileID=2, current_lobby=lobby)))