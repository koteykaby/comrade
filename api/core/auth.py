from api.protocols.game.login import platformlogin

from api.database.interract import *
from api.database.scripts.create_account import create_account

from api.core.sessions import *

import json

# configurations
server_values = json.load(open('data/values.json'))
server_config = json.load(open('config/config.json'))
client_config = json.load(open('data/reliclink.json'))

user_session_id_counter = 0

def steam_create(steamid):
    create_account(steamID=steamid,
                   country='ru')

def steam_auth(steamid,
               username):
    account_data = get_userdata(steamid=steamid)
    if account_data.data['account_ban']['expiryDate'] == -1:
        banState = None
        
    global user_session_id_counter
    user_session_id_counter+=1
    
    data=platformlogin.do_platformlogin(username=username,
                                        sessionid=user_session_id_counter,
                                        last_matchID=server_values['counters']['match_id'],
                                        cfg_b=server_config['battleserver'],
                                        client_config=client_config,
                                        profileid=account_data.id,
                                        statgroupid=account_data.id,
                                        u_rlink=account_data.data['reliclink'],
                                        u_profile=account_data.data['profile_info'],
                                        u_leaderboardStats=account_data.data['leaderboardStats'],
                                        u_stats=account_data.data['stats'],
                                        u_playerData=account_data.data['player_data'],
                                        banState=banState)
    
    client_sessionCreate(sessionID=str(user_session_id_counter),
                         accountID=account_data.id)
    
    return data
