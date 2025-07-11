from api.protocols.game.login.structures import PresenceProfile
from dataclasses import dataclass

@dataclass
class FindProfilesByPlatformID:
    status_code: int
    p: PresenceProfile
    
def account_FindProfilesByPlatformID(profiles):
    data = []
    for item in data:
        profile = PresenceProfile(**item)
        data.append(profile)
        print(data)
    result = FindProfilesByPlatformID(
        status_code=0,
        p=data
    )
    return result