from dataclasses import dataclass
from time import time
from api.protocols.game.login.structures import *

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
    
def do_platformlogin(username,
                     sessionid,
                     last_matchID,
                     cfg_b,
                     client_config,
                     profileid,
                     statgroupid,
                     u_rlink,
                     u_profile,
                     u_leaderboardStats,
                     u_stats,
                     u_playerData, 
                     banState):
    
    result = platformlogin(
            unk=0,
            sessionID=str(sessionid),
            matchID=last_matchID,
            auth_time=int(time()),
            rlink_account=rlink_info(
                **u_rlink, id=profileid
            ),
            profileinfo=[profile(
                **u_profile, alias=username, id=profileid, personalStatGroupID=statgroupid, banInfo=banState
            )],
            unk1=0,
            unk2=0,
            unk3=None,
            unk4=[],
            config=client_config,
            playerdata=(
                0,
                profile(**u_profile, alias=username, id=profileid, personalStatGroupID=statgroupid, banInfo=banState),
                [0,[],[],[],[],[],[],[]], # friends field?
                [list(obj.values()) for obj in u_leaderboardStats],
                [list(obj.values()) for obj in u_stats],
                None,
                u_playerData['categoryIDs'],
                str(u_playerData['characterData']),
                u_playerData['enableCrossplay'],
                u_playerData['privacySettings']
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
    return result