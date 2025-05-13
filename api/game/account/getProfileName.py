import json
from api.structures.p_struct import profile
from dataclasses import dataclass

@dataclass
class get_profile_name:
    unk: int
    p: profile

def getProfileName(steamid,
                   username):
    with open(f'db/{steamid}.json', 'r') as f:
        account_data = json.load(f)
        f.close()
        
    u_profile = account_data['defaultProfileInfo']
    
    result = get_profile_name(
        unk=0,
        p=[profile(
            **u_profile, alias=username
        )]
    )
    return result