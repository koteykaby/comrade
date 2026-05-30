import asyncio

from common.logger import logger
from singletons import servicesConfig

from managers import matchmaking, sessions

DEFAULT_INTERVAL_SECONDS = 60
DEFAULT_SESSION_TTL_SECONDS = 30 * 60
DEFAULT_EMPTY_LOBBY_GRACE_SECONDS = 30


def _get_cleanup_config() -> tuple[int, int, int]:
    cleanup_config = servicesConfig.get("cleanup", {})
    return (
        cleanup_config.get("intervalSeconds", DEFAULT_INTERVAL_SECONDS),
        cleanup_config.get("sessionTtlSeconds", DEFAULT_SESSION_TTL_SECONDS),
        cleanup_config.get("emptyLobbyGraceSeconds", DEFAULT_EMPTY_LOBBY_GRACE_SECONDS),
    )


def run_cleanup_once() -> None:
    _, session_ttl, lobby_grace = _get_cleanup_config()

    expired_sessions = sessions.CleanupExpiredSessions(session_ttl)
    if expired_sessions:
        logger.info(f"Cleaned up {len(expired_sessions)} expired session(s)")

    referenced_lobby_ids = sessions.GetReferencedAdvertisementIds()
    deleted_lobbies = matchmaking.CleanupEmptyAdvertisements(referenced_lobby_ids, lobby_grace)
    if deleted_lobbies:
        logger.info(f"Cleaned up {len(deleted_lobbies)} empty lobby/lobbies: {deleted_lobbies}")


async def cleanup_loop() -> None:
    interval, session_ttl, _ = _get_cleanup_config()
    logger.info(
        f"Session and lobby cleanup started (every {interval}s, "
        f"session TTL {session_ttl}s)"
    )

    while True:
        try:
            run_cleanup_once()
        except Exception as error:
            logger.error(f"Cleanup task failed: {error}")
        await asyncio.sleep(interval)
