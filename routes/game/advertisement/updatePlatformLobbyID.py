from common.logger import logger

from managers import matchmaking, sessions

async def Handle(sessionID: str, matchID: int, platformLobbyID: int):
    logger.info(f"UpdatePlatformLobbyID called with matchID: {matchID}, platformLobbyID: {platformLobbyID}")
    
    adv = await matchmaking.GetAdvertisement(matchID)
    
    if adv is not None:
        adv["platformLobbyID"] = platformLobbyID
        logger.debug(f"Updated advertisement: {adv}")
        
    sessions.AddNotification(sessionID, "PlatformSessionUpdateMessage")
    
    return [0]