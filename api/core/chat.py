from api.protocols.game.chat.getOfflineMessages import getOfflineMessages
from api.protocols.game.chat.sendMatchChat import chat_sendMatchChat
from api.core.sessions import sessions_data

def resp_getOfflineMessages(sessionID): 
    session_data = sessions_data[f'{sessionID}']
    id = session_data['account']
    result = getOfflineMessages(id)
    return result

def resp_sendMatchChat():
    result = chat_sendMatchChat()
    return result