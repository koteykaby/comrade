from dataclasses import dataclass
import json
from api.structures.p_struct import *
from api.utils.datautils import *
from api.main import storage
import time

cfg_rl = json.load(open('data/reliclink.json', 'r'))
cfg = json.load(open('config/config.json', 'r'))
cfg_b = cfg['battleserver']

@dataclass
class player_data:
    unk: int
    profileinfo: profile

@dataclass
class platformlogin:
    unk: int 
    sessionID: str
    matchID: int
    auth_time: int 
    
    rlink_account: rlink_info # data
    profileinfo: profile
    
    unk1: int # ???
    unk2: int
    unk3: None
    unk4: list
    
    config: any # data/reliclink.json
    playerdata: any
    unk5: list
    unk6: int
    battleserver: any
    
def authorize(steamid=str,
              username=str,
              sid=str,
              mid=int,
              atime=int(time.time())):
    with open(f'db/{steamid}.json', 'r') as f:
        account_data = json.load(f)
        f.close()
        
    u_rlink = account_data['rlink']
    u_profile = account_data['defaultProfileInfo']
    u_leaderboards = account_data['leaderboardStats']
    u_stats = account_data['stats']
    u_playerdata = account_data['playerdata']
    
    result = platformlogin(
            unk=0,
            sessionID=str(sid),
            matchID=mid,
            auth_time=atime,
            rlink_account=rlink_info(
                **u_rlink
            ),
            profileinfo=[profile(
                **u_profile, alias=username
            )],
            unk1=0,
            unk2=0,
            unk3=None,
            unk4=[],
            config=cfg_rl,
            playerdata=(
                0,
                profile(**u_profile, alias=username),
                [0,[],[],[],[],[],[],[]], # friends field?
                [list(obj.values()) for obj in u_leaderboards],
                [list(obj.values()) for obj in u_stats],
                None,
                u_playerdata['categoryIDs'],
                u_playerdata['characterData'],
                u_playerdata['enableCrossplay'],
                u_playerdata['privacySettings']
            ),
            unk5=[],
            unk6=0,
            battleserver=(
                [
                    cfg_b['name'],
                    None,
                    cfg_b['address'],
                    cfg_b['ports'][0],
                    cfg_b['ports'][1],
                    cfg_b['ports'][2]
                ],
                [
                    cfg_b['name'],
                    None,
                    cfg_b['address'],
                    cfg_b['ports'][0],
                    cfg_b['ports'][1],
                    cfg_b['ports'][2]
                ],
                [
                    cfg_b['name'],
                    None,
                    cfg_b['address'],
                    cfg_b['ports'][0],
                    cfg_b['ports'][1],
                    cfg_b['ports'][2]
                ]
            )
        )
    storage.create_session(steamID=steamid,
                           username=username,
                           profileID=u_profile['id'],
                           sessionid=sid)

    return result