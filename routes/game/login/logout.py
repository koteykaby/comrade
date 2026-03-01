from managers import sessions

async def Handle(sessionID):
    sessions.DeleteSession(sessionID)
    
    return [0]