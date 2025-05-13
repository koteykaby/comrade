from dataclasses import dataclass
from api.structures.p_struct import PresenceProfile
import json

@dataclass
class PresenceMessage:
    unk: int
    description: str
    profileid: int
    data: any
    
def CreatePresenceMessage(steamid,
                          username):
    with open(f'db/{steamid}.json', 'r') as f:
        account_data = json.load(f)
        f.close()
        
    u_profile = account_data['defaultProfileInfo']
    
    result = [[PresenceMessage(
        unk=0,
        description="PresenceMessage",
        profileid=u_profile['id'],
        data=[PresenceProfile(
            **u_profile, 
            alias=username,
            presenceID=1,
            presenceLocalized=None,
            presencePropertyInfo=[]
        )
        ]
    )]]
    return result