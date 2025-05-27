from api.protocols.game.account.getProfileName import *

from api.database import interract
from api.core.sessions import sessions_data

from api.utils.datautils import relicjson

def data_getProfileName(sessionID):
    account_data = interract.get_userdata(account_id=sessions_data[f'{sessionID}']['account'])
    session_data = sessions_data[f'{sessionID}']
    banState = account_data.data['account_ban']['expiryDate']
    if banState == -1:
        ban = None
        
    data = getProfileName(u_profile=account_data.data['profile_info'],
                          username=session_data['username'],
                          profileid=session_data['account'],
                          banInfo=ban)
    print(data)
    return relicjson(data)