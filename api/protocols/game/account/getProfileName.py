from api.protocols.game.login.structures import profile
from dataclasses import dataclass

@dataclass
class GetProfileNameResponse:
    status_code: int
    data: any  

def getProfileName(u_profile, id, banInfo):
    profile_obj = profile(**u_profile, id=id, banInfo=banInfo, personalStatGroupID=id)
    result = GetProfileNameResponse(
        status_code=0,
        data=[None, profile_obj]
    )
    return result