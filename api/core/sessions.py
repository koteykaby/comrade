from api.protocols.game.login import readSession
from api.database import interract
from api.utils.datautils import relicjson
import json
import asyncio 

sessions_data = {}
clients_list = []

def client_sessionCreate(sessionID=str, accountID=int, username=str):
    data = interract.get_userdata(account_id=accountID)
    account_info = data.data
    account = account_info['profile_info']
    
    inventory = []
    for item in data.inventory:
        if item['locationID'] != 0:
            meta_data = item['metaData'].replace('\\\\', '\\') if item['metaData'] else ""
            inventory.append([
                item['id'],
                item['entityVersion'],
                item['itemDefinition.id'],
                item['profileID'],
                item['durability'],
                item['durabilityType'],
                meta_data,  
                item['creationDate'],
                item['locationID'],
                item['tradeID'],
                item['permission'],
                item['maxChargesPerItem']
            ])
    
    if account_info['account_ban']['expiryDate'] == -1:
        banState = None
    else:
        banState = account_info['account_ban']
    
    memory = {
        sessionID: {
            "account": accountID,
            "username": username,
            #"equipped_items": inventory  
        }
    }
    client = {
        "entityVersion": account['entityVersion'],
        "id": accountID,
        "name": account['name'],
        "metaData": account['metaData'],
        "alias": username,
        "clanName": account['clanName'],
        "personalStatGroupID": accountID,
        "xp": account['xp'],
        "level": account['level'],
        "leaderboardRegionID": account['leaderboardRegionID'],
        "banInfo": banState,
        "platformUserID": account['platformUserID'],
        "accountType": account['accountType'],
        "linkedPlatformAccount": account['linkedPlatformAccounts'],
        "presenceID": 0,
        "presenceLocalized": None,
        "presencePropertyInfo": []
    }
    
    global sessions_data
    global clients_list
    sessions_data.update(memory)
    clients_list.append(client)
    print(clients_list)
    print("[Core.Sessions] New session!")

    
def client_sessionClear(sessionID):
    global sessions_data
    if sessionID in sessions_data:
        del sessions_data[f'{sessionID}']
        print(f'[Core.Sessions] Session with ID {sessionID} is cleared!')
    else:
        print('[Core.Sessions] ERROR! Session is not found.')

async def readSession_Emptiness(sessionID, ack):
    data = readSession.do_EmptyRead()
    result = f'{ack},{data}'
    print(f'[Core.Sessions] Keeping Session {sessionID} alive')
    await asyncio.sleep(10)  
    return result

async def readSession_PresenceMessage(sessionID, ack):
    account_data = interract.get_userdata(account_id=sessions_data[f'{sessionID}']['account'])
    session_data = sessions_data[f'{sessionID}']
    banState = account_data.data['account_ban']['expiryDate']
    if banState == -1:
        ban = None
    if ack == 0:
        data = readSession.do_PresenceMessage(profileid=session_data['account'],
                                              u_profile=account_data.data['profile_info'],
                                              banInfo=ban)
        result = f'{ack+1},{data}'
        print(data)
        print(f'[Core.Sessions] client_readSession_handle() -> PresenceMessage for Session:{sessionID}')
        return result

async def readSession_PlatformSessionUpdateMessage(sessionID, ack):
    session_data = sessions_data[f'{sessionID}']
    if 'lobby_info' in session_data:
        lobbyid = session_data['lobby_info']['id']
        platformlobbyid = session_data['lobby_info']['platformLobbyID']
    data = readSession.do_PlatformSessionUpdateMessage_ReadSessionMessage(profileid=session_data['account'],
                                                                          lobbyid=lobbyid,
                                                                          platformlobbyid=platformlobbyid)
    result = f'{ack+1},{relicjson(data)}'
    print(result)
    return result

async def readSession_MatchStartMessage(sessionID, ack): # appears when match starting
    session_data = sessions_data[f'{sessionID}']
    if session_data['lobby_info']['MatchStarted'] == True:
        data = readSession.do_MatchStartMessage(profileID=session_data['account'])
        result = f'{ack+1},{relicjson(data)}'
        return result
    
#async def readSession_MatchHostedMessage(sessionID, ack) # appears when lobby host is changed
    #session_data = sessions_data[f'{sessionID}']
    #if sessionID['lobby_info']['isHost']
    
async def client_readSession_handle(sessionID, ack):
    global result
    # getting session data
    try:
        session_data = sessions_data[f'{sessionID}']
        print(json.dumps(session_data, indent=4))
    except KeyError:
        print(f'[Core.Sessions] WARNING: Session {sessionID} is not found!')
    # and handling this request    
    if ack == 0: 
        result = await readSession_PresenceMessage(sessionID=sessionID, ack=ack)
    elif ack != 0:
        if 'lobby_info' in session_data and session_data['lobby_info'].get('logged') == True:
            if session_data['lobby_info'].get('platformLobbyID') is not None:
                # changing platformLobbyID
                result = await readSession_PlatformSessionUpdateMessage(sessionID=sessionID, ack=ack) 
                print(result) 
                print(f"UPDATED STATE FOR SESSION ID {sessionID}") 
                del session_data['lobby_info']['logged']  
            if session_data['lobby_info'].get('MatchStarted') is True:
                print(f"[Core.Sessions] readSession -> MatchStartMessage session {sessionID}")
                # trying to start match!
                result = await readSession_MatchStartMessage(sessionID=sessionID, ack=ack) 
                print(result) 
                return result
        else:
            result = await readSession_Emptiness(sessionID=sessionID, ack=ack)
    else:
        result = 'error'
    return result
