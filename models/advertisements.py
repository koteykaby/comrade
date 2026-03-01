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
class Advertisement:
    advertisementid: int
    platformLobbyID: int
    unknown: str
    hostid: int
    state: int
    description: str
    visible: int
    mapname: str
    options: str
    passworded: int
    maxplayers: int
    slotinfo: str
    matchtype: int
    peers: list[Peer]
    unk: int
    unk1: int
    isObservable: int
    observerDelay: int
    unk4: int
    unk5: int 
    startGameTime: None
    relayRegion: str
    endGameTime: None