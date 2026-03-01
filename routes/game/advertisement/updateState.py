from common.logger import logger

from managers import matchmaking, sessions

async def Handle(advertisementid, state):
    logger.info(f"UpdateState called for advertisement ID: {advertisementid} with new state: {state}")
    
    adv = await matchmaking.GetAdvertisement(int(advertisementid))
    
    if adv is None:
        logger.info(f"Advertisement {advertisementid} not found for state update")
        return [0]
    
    # Updating state
    adv["state"] = int(state)
    
    for peer in adv["peers"]:
        logger.info(f"Notifying peer: {peer}")
        p_id = peer.get("profileID")
        if p_id:
            sessions.AddNotificationByProfileID(p_id, "MatchStartMessage")

    return [0]