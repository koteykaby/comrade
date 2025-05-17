from api.protocols.game.account.getProfileName import *

from api.databases import db, interract
from api.core.sessions import sessions_data

db_session = db.create_session()

def data_getProfileName(sessionID):
    account_data = interract.get_account_data(db_session=db_session,
                                              account_id=sessions_data[f'{sessionID}']['account'])
    session_data = sessions_data[f'{sessionID}']
    banState = account_data['account_ban']['expiryDate']
    if banState == -1:
        ban = None
        
    data = getProfileName(u_profile=account_data['profile_info'],
                          username=session_data['username'],
                          profileid=session_data['account'],
                          banInfo=ban)
    return data