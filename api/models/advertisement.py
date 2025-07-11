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
class Lobby:
    id: int
    platformlobbyid: int
    unk: str # "0"
    hostid: int
    state: int # 0
    description: str # "SESSION_MATCH_KEY"
    visible: int 
    mapname: str
    options: str
    passworded: int
    maxplayers: int
    slotinfo: str
    matchType: int
    peers: list[Peer]
    unk2: int # 0
    unk3: int # 512
    isObservable: int
    observerDelay: int
    unk4: int
    unk5: int
    startGameTime: None
    relayRegion: str
    endGameTime: None