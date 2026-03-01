from managers.sessions import GetSession
from managers.account import GetAccount

async def Handle(sessionID: str):
    sessionData = GetSession(sessionID)
    
    userData = GetAccount(sessionData["platformUserID"])
    
    result = [0,[],[[userData["profileInfo"]["id"],[]]],[],[],[]]
    
    return result