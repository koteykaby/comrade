from dataclasses import dataclass, astuple
from time import time

from common.serialize import relicjson

from models.user import accountInfo, profileInfo, additionalProfileInfo
from models.services import battleserver

from managers.sessions import CreateSession
from managers.account import GetAccount, db_manager
from managers.matchmaking import lastMatchID

from singletons import reliclinkConfig, servicesConfig

@dataclass
class response:
    result: int
    sessionID: str
    lastMatchID: int
    authTime: int
    rlinkAccount: accountInfo
    profiles: list[profileInfo]
    unk1: int
    unk2: int
    unk3: None
    unk4: list
    rlinkConfig: list
    additional: additionalProfileInfo
    unk5: list
    unk6: int
    battleservers: list[battleserver]
    
def _parse_battleservers(data: dict) -> list[battleserver]:
    raw_servers = data.get("battleservers", [])
    parsed: list[battleserver] = []

    for srv in raw_servers:
        parsed.append(
            battleserver(
                region=srv["region"],
                name=srv.get("name"),
                ipv4=srv["address"],
                bsPort=srv["ports"]["bs_port"],
                webSocketPort=srv["ports"]["websocket_port"],
                outOfBandPort=srv["ports"]["out_of_band_port"],
            )
        )

    if not parsed:
        raise ValueError("battleservers list is empty")

    while len(parsed) < 3:
        parsed.append(parsed[0])

    return parsed[:3]
    
def Handle(platformUserID: str, alias: str):
    userData = GetAccount(platformUserID)
    
    if not userData:
        print(f"User {platformUserID} not found. Registering as '{alias}'...")
        userData = db_manager.create_account(platformUserID, alias)
        
        if not userData:
             raise Exception("Failed to create user account database record.")

    sessionID = CreateSession(platformUserID)
    
    additional = additionalProfileInfo(
        result=0,
        profile=profileInfo(**userData["profileInfo"]),
        social=[0,[],[],[],[],[],[],[]], # i have no friends :(
        leaderboardStats=[([userData["profileInfo"]["personalStatGroupID"],1,33,1,3,0,1,-1,-1,-1,-1,-1,1000,"{}","{}",1740504208]) for i in range (1, 4)],
        otherStats=[(i, userData["profileInfo"]["id"], 5, "", 1740504207) for i in range(1, 11)],
        unknownNull=None,
        categoryIDs=userData["categoryIDs"],
        characterData=str([userData["characterData"]]),
        enableCrossplay=userData["enableCrossplay"],
        privacySettings=userData["privacySettings"]
    )
        
    result = response(
        result=0,
        sessionID=sessionID,
        lastMatchID=lastMatchID,
        authTime=int(time()),
        rlinkAccount=accountInfo(**userData["rlinkAccountInfo"]),
        profiles=[profileInfo(**userData["profileInfo"])],
        unk1=0,
        unk2=0,
        unk3=None,
        unk4=[],
        rlinkConfig=reliclinkConfig,
        additional=additional,
        unk5=[],
        unk6=0,
        battleservers=_parse_battleservers(servicesConfig)
    )
    
    return astuple(result)