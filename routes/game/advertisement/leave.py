from common.logger import logger
from managers import sessions, matchmaking, account

async def Handle(sessionID, advertisementID):
    try:
        session = sessions.GetSession(sessionID)
        userData = account.GetAccount(session["platformUserID"])
    except KeyError:
        logger.error(f"RemovePeer: Session {sessionID} not found")
        return False

    profile_id = userData["profileInfo"].get("id") # type: ignore
    
    if profile_id is None:
        logger.error(f"RemovePeer: Profile ID not found in session {sessionID}")
        return False

    advertisement = await matchmaking.GetAdvertisement(advertisementID)
    if not advertisement:
        logger.error(f"RemovePeer: Advertisement {advertisementID} not found")
        return False

    initial_peer_count = len(advertisement["peers"])
    
    advertisement["peers"] = [
        peer for peer in advertisement["peers"] 
        if peer["profileID"] != int(profile_id)
    ]

    if len(advertisement["peers"]) < initial_peer_count:
        logger.debug(f"Removed peer {profile_id} from lobby {advertisementID}")
        
        sessions.RemoveFromAdvertisement(sessionID)
        
        if len(advertisement["peers"]) == 0:
           await matchmaking.DeleteAdvertisement(advertisementID)
        
        return True
    else:
        logger.warning(f"RemovePeer: Peer {profile_id} was not found in lobby {advertisementID}")
        return False