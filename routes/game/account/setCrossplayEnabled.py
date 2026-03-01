from common.logger import logger

from managers.account import GetAccount
from managers.sessions import GetSession

async def Handle(sessionID: str, enabled: int):
    sessionData = GetSession(sessionID)
    
    userData = GetAccount(sessionData["platformUserID"])
    userData["crossplayEnabled"] = int(enabled) # type: ignore
    
    logger.info(f"{userData['rlinkAccountInfo']['accountName']} crossplayEnabled set to {enabled}") # type: ignore
    
    return [0]