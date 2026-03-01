from dataclasses import dataclass, astuple
import json
from managers import account
from models.user import profileInfo
from common.logger import logger

@dataclass
class response:
    result: int
    profileNames: list[profileInfo]

async def Handle(profileIDs):
    ids = json.loads(profileIDs)
    
    found_profiles = []
    
    for pid in ids:
        acc_data = account.GetAccountByProfileID(int(pid))
        
        if acc_data and "profileInfo" in acc_data:
            found_profiles.append(
                profileInfo(**acc_data["profileInfo"])
            )
        else:
            logger.warning(f"Profile ID {pid} not found, skipping.")
            pass

    result = response(
        result=0,
        profileNames=found_profiles
    )
    
    return json.dumps(result, separators=(",", ":"), default=astuple)