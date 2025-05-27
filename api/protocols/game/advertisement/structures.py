from dataclasses import dataclass

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
    