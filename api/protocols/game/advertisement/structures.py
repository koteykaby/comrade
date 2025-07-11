from dataclasses import dataclass
from api.models.advertisement import Lobby

@dataclass
class Peer:
    advertisementID: int
    profileID: int
    party: int
    statGroupID: int
    raceID: int
    team: int
    route: str
    
@dataclass
class battleserver_authtoken:
    status_code: int
    advertisementid: int
    description: str
    address: str
    port1: int
    port2: int
    port3: int
    relayRegion: str
    peerList: any
    unk: int
    unk1: str
    
@dataclass
class AdvertisementsList:
    status_code: int
    advertisements: any
    unknown_null: list
    
@dataclass
class get_advertisements_resp:
    status_code: int
    advertisements: any
    
@dataclass
class join_advertisement_resp:
    status_code: int
    route: str
    address: str
    port1: int
    port2: int
    port3: int
    peers: any