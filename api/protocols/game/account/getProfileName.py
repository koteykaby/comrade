from api.protocols.game.login.structures import profile
from dataclasses import dataclass

from api.core.utils.datautils import relicjson

@dataclass
class get_profile_name:
    unk: int
    p: profile

def getProfileName(u_profile,
                   username,
                   profileid,
                   banInfo):
    result = get_profile_name(
        unk=0,
        p=[profile(
            **u_profile,
            id=profileid, 
            alias=username,
            personalStatGroupID=profileid,
            banInfo=banInfo
        )]
    )
    return relicjson(result)