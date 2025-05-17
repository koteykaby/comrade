from api.protocols.game.login import readSession

from api.databases import db, interract

from time import sleep

sessions_data = {}
db_session = db.create_session()

def client_sessionCreate(sessionID=str, accountID=int, username=str):
    memory = {
        sessionID: {
            "account": accountID,
            "username": username
        }
    }
    global sessions_data
    sessions_data.update(memory)
    
def client_sessionClear(sessionID):
    global sessions_data
    if sessionID in sessions_data:
        del sessions_data[f'sessionID']
        print(f'[Core.Sessions] Session with ID {sessionID} is cleared!')
    else:
        print('[Core.Sessions] ERROR! Session is not found.')
    
def readSession_Emptiness(sessionID, ack):
    data = readSession.do_EmptyRead()
    result = f'{ack},{data}'
    print(f'[Core.Sessions] client_readSession_handle() -> Keeping Session {sessionID} alive')
    sleep(10)
    return result

def readSession_PresenceMessage(sessionID, ack):
    account_data = interract.get_account_data(db_session=db_session,
                                              account_id=sessions_data[f'{sessionID}']['account'])
    session_data = sessions_data[f'{sessionID}']
    banState = account_data['account_ban']['expiryDate']
    if banState == -1:
        ban = None
    if ack == 0:
        data = readSession.do_PresenceMessage(profileid=session_data['account'],
                                              u_profile=account_data['profile_info'],
                                              username=session_data['username'],
                                              banInfo=ban)
        result = f'{ack+1},{data}'
        print(f'[Core.Sessions] client_readSession_handle() -> PresenceMessage for Session:{sessionID}')
        return result
    
def client_readSession_handle(sessionID, ack):
    if ack == 0: 
        result = readSession_PresenceMessage(sessionID=sessionID, ack=ack)
    elif ack != 0:
        result = readSession_Emptiness(sessionID=sessionID, ack=ack)
    else:
        result = 'error'
    return result