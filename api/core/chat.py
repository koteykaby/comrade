from api.protocols.game.chat.getOfflineMessages import getOfflineMessages

from api.databases import db, interract
from api.core.sessions import sessions_data

db_session = db.create_session()

def resp_getOfflineMessages(sessionID): 
    session_data = sessions_data[f'{sessionID}']
    id = session_data['account']
    result = getOfflineMessages(id)
    return result