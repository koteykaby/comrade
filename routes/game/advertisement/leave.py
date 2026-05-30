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

    if matchmaking.RemovePeerFromAdvertisement(advertisementID, int(profile_id)):
        logger.debug(f"Removed peer {profile_id} from lobby {advertisementID}")
        sessions.RemoveFromAdvertisement(sessionID)

        if not advertisement["peers"]:
            await matchmaking.DeleteAdvertisement(advertisementID)

        return True

    logger.warning(f"RemovePeer: Peer {profile_id} was not found in lobby {advertisementID}")
    return False
