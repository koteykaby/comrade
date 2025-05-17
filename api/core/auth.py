from api.protocols.game.login import platformlogin

from api.databases.db import *
from api.databases.interract import *

from api.core.sessions import *

import json

# configurations
server_values = json.load(open('data/values.json'))
server_config = json.load(open('config/config.json'))
client_config = json.load(open('data/reliclink.json'))

user_session_id_counter = 0

db_session = create_session()

def steam_create(steamid):
    create_account(db_session=db_session,
                   steamID=steamid,
                   country='ru')

def steam_auth(steamid,
               username):
    account_data = get_account_data(db_session=db_session,
                                    steamid=steamid)
    account_id = get_account_id(db_session=db_session,
                                steamid=steamid)
    if account_data['account_ban']['expiryDate'] == -1:
        banState = None
        
    global user_session_id_counter
    user_session_id_counter+=1
    
    data=platformlogin.do_platformlogin(username=username,
                                        sessionid=user_session_id_counter,
                                        last_matchID=server_values['counters']['match_id'],
                                        cfg_b=server_config['battleserver'],
                                        client_config=client_config,
                                        profileid=account_id,
                                        statgroupid=account_id,
                                        u_rlink=account_data['reliclink'],
                                        u_profile=account_data['profile_info'],
                                        u_leaderboardStats=account_data['leaderboardStats'],
                                        u_stats=account_data['stats'],
                                        u_playerData=account_data['player_data'],
                                        banState=banState)
    
    client_sessionCreate(sessionID=str(user_session_id_counter),
                         accountID=account_id)
    
    return data
