from dataclasses import dataclass
from api.protocols.game.login.structures import PresenceProfile, PlatformSessionUpdateMessage

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
                       username,
                       banInfo):        
    result = [[PresenceMessageStruct(
        unk=0,
        description="PresenceMessage",
        profileid=profileid,
        data=[PresenceProfile(
            **u_profile,
            id=profileid, 
            alias=username,
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