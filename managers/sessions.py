import secrets
import string
from collections import deque

from common.logger import logger

from managers import account

sessions = {}

def _generate_session_id(length=30) -> str:
    alphabet = string.ascii_lowercase + string.digits  # a-z0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def CreateSession(platformUserID: str) -> str:
    sessionID = _generate_session_id()
    
    userData = account.GetAccount(platformUserID)
    
    sessions[sessionID] = {
        "platformUserID": platformUserID,
        "profileInfo": userData["profileInfo"],
        "ack": 0,
        "notifications": deque(["PresenceMessage"]) # ExtensionMessage was also here
    }
    
    logger.info(f"New session: {sessionID}:{platformUserID}")
    #logger.debug(f"Current sessions: {sessions}")
    
    return sessionID

def GetSession(sessionID: str) -> dict:
    return sessions[sessionID]

def GetSessionByProfileID(profileID: int):
    for s in sessions.values():
        if s['profileInfo']['id'] == profileID:
            logger.info(f"Found session by profileID {profileID}!")
            return s

def AddNotification(sessionID: str, notification: str):
    sessionData = GetSession(sessionID)
    
    logger.debug(f"Adding notification to session {sessionID}: {notification}")
    
    sessionData["notifications"].append(notification)
    
def AddNotificationByProfileID(profileID: int, notification: str):
    target_session = None
    
    for s_id, data in sessions.items():
        try:
            if int(data["profileInfo"].get("id", -1)) == int(profileID):
                target_session = data
                break
        except (ValueError, TypeError):
            continue
            
    if target_session:
        logger.debug(f"Sending {notification} to profile {profileID}")
        target_session["notifications"].append(notification)
        return True
    else:
        logger.warning(f"AddNotificationByProfileID: Session for profile {profileID} not found.")
        return False
    
def AddToAdvertisement(sessionID: str, advertisementID: int):
    sessionData = GetSession(sessionID)
    
    sessionData["advertisement"] = {
        "id": advertisementID
    }
    
def RemoveFromAdvertisement(sessionID: str):
    try:
        sessionData = GetSession(sessionID)
        if "advertisement" in sessionData:
            del sessionData["advertisement"]
            logger.debug(f"Session {sessionID} removed from advertisement reference.")
    except KeyError:
        pass
    
def DeleteSession(sessionID: str) -> bool:
    if sessionID in sessions:
        del sessions[sessionID]
        logger.info(f"Session deleted: {sessionID}")
        logger.debug(f"Remaining sessions: {len(sessions)}")
        return True
    else:
        logger.warning(f"DeleteSession: Attempted to delete non-existent session {sessionID}")
        return False
    
def GetSessionInventoryByProfileID(profileID: int):
    s = GetSessionByProfileID(profileID)
    
    return s["equipedItems"]