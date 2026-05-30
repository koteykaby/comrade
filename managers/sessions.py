import secrets
import string
import time
from collections import deque

from common.logger import logger

from managers import account

SESSION_ID_LENGTH = 30
DEFAULT_NOTIFICATIONS = ("PresenceMessage",)

def _generate_session_id(length: int = SESSION_ID_LENGTH) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _profile_id_from_session(session_data: dict) -> int | None:
    try:
        return int(session_data["profileInfo"].get("id", -1))
    except (ValueError, TypeError):
        return None


class SessionManager:
    def __init__(self):
        self.sessions: dict[str, dict] = {}

    def create_session(self, platform_user_id: str) -> str:
        session_id = _generate_session_id()
        user_data = account.GetAccount(platform_user_id)
        now = time.time()

        self.sessions[session_id] = {
            "platformUserID": platform_user_id,
            "profileInfo": user_data["profileInfo"],
            "ack": 0,
            "notifications": deque(DEFAULT_NOTIFICATIONS),
            "createdAt": now,
            "lastActiveAt": now,
        }
        logger.info(f"New session: {session_id}:{platform_user_id}")
        return session_id

    def get_session(self, session_id: str) -> dict:
        session_data = self.sessions[session_id]
        session_data["lastActiveAt"] = time.time()
        return session_data

    def touch_session(self, session_id: str) -> None:
        session_data = self.sessions.get(session_id)
        if session_data is not None:
            session_data["lastActiveAt"] = time.time()
    def get_session_by_profile_id(self, profile_id: int) -> dict | None:
        session_data = self._find_session_by_profile_id(profile_id)
        if session_data is not None:
            logger.info(f"Found session by profileID {profile_id}!")
        return session_data

    def add_notification(self, session_id: str, notification: str) -> None:
        session_data = self.get_session(session_id)
        logger.debug(f"Adding notification to session {session_id}: {notification}")
        session_data["notifications"].append(notification)

    def add_notification_by_profile_id(self, profile_id: int, notification: str) -> bool:
        session_data = self._find_session_by_profile_id(profile_id)
        if session_data is None:
            logger.warning(
                f"AddNotificationByProfileID: Session for profile {profile_id} not found."
            )
            return False

        logger.debug(f"Sending {notification} to profile {profile_id}")
        session_data["notifications"].append(notification)
        return True

    def add_to_advertisement(self, session_id: str, advertisement_id: int) -> None:
        session_data = self.get_session(session_id)
        session_data["advertisement"] = {"id": advertisement_id}

    def remove_from_advertisement(self, session_id: str) -> None:
        try:
            session_data = self.get_session(session_id)
            if "advertisement" in session_data:
                del session_data["advertisement"]
                logger.debug(f"Session {session_id} removed from advertisement reference.")
        except KeyError:
            pass

    def delete_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session deleted: {session_id}")
            logger.debug(f"Remaining sessions: {len(self.sessions)}")
            return True

        logger.warning(f"DeleteSession: Attempted to delete non-existent session {session_id}")
        return False

    def get_session_inventory_by_profile_id(self, profile_id: int):
        session_data = self.get_session_by_profile_id(profile_id)
        return session_data["equipedItems"]

    def get_referenced_advertisement_ids(self) -> set[int]:
        referenced_ids: set[int] = set()
        for session_data in self.sessions.values():
            advertisement_ref = session_data.get("advertisement")
            if advertisement_ref:
                referenced_ids.add(int(advertisement_ref["id"]))
        return referenced_ids

    def cleanup_expired_sessions(self, max_age_seconds: float) -> list[str]:
        now = time.time()
        expired_session_ids = [
            session_id
            for session_id, session_data in self.sessions.items()
            if now - session_data.get("lastActiveAt", session_data.get("createdAt", now))
            > max_age_seconds
        ]

        deleted_session_ids: list[str] = []
        for session_id in expired_session_ids:
            self._cleanup_session_lobby_membership(session_id)
            if self.delete_session(session_id):
                deleted_session_ids.append(session_id)

        return deleted_session_ids

    def _cleanup_session_lobby_membership(self, session_id: str) -> None:
        from managers import matchmaking

        session_data = self.sessions.get(session_id)
        if session_data is None:
            return

        advertisement_ref = session_data.get("advertisement")
        profile_id = _profile_id_from_session(session_data)
        if advertisement_ref is None or profile_id is None:
            return

        matchmaking.RemovePeerFromAdvertisement(
            int(advertisement_ref["id"]),
            profile_id,
        )
    def _find_session_by_profile_id(self, profile_id: int) -> dict | None:
        target_profile_id = int(profile_id)
        for session_data in self.sessions.values():
            session_profile_id = _profile_id_from_session(session_data)
            if session_profile_id == target_profile_id:
                return session_data
        return None


_manager = SessionManager()

sessions = _manager.sessions


def CreateSession(platformUserID: str) -> str:
    return _manager.create_session(platformUserID)


def GetSession(sessionID: str) -> dict:
    return _manager.get_session(sessionID)


def GetSessionByProfileID(profileID: int):
    return _manager.get_session_by_profile_id(profileID)


def AddNotification(sessionID: str, notification: str):
    _manager.add_notification(sessionID, notification)


def AddNotificationByProfileID(profileID: int, notification: str):
    return _manager.add_notification_by_profile_id(profileID, notification)


def AddToAdvertisement(sessionID: str, advertisementID: int):
    _manager.add_to_advertisement(sessionID, advertisementID)


def RemoveFromAdvertisement(sessionID: str):
    _manager.remove_from_advertisement(sessionID)


def DeleteSession(sessionID: str) -> bool:
    return _manager.delete_session(sessionID)


def GetSessionInventoryByProfileID(profileID: int):
    return _manager.get_session_inventory_by_profile_id(profileID)


def TouchSession(sessionID: str) -> None:
    _manager.touch_session(sessionID)


def GetReferencedAdvertisementIds() -> set[int]:
    return _manager.get_referenced_advertisement_ids()


def CleanupExpiredSessions(max_age_seconds: float) -> list[str]:
    return _manager.cleanup_expired_sessions(max_age_seconds)