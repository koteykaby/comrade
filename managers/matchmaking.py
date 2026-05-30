import json
import time
from typing import Any
from common.logger import logger

DEFAULT_ROUTE = "/10.0.7.136"
INITIAL_MATCH_ID = 31005

_UPDATE_FIELDS = (
    "hostid", "state", "description", "visible", "mapname", "options",
    "passworded", "maxplayers", "slotinfo", "matchtype",
    "isObservable", "observerDelay",
)
_INT_UPDATE_FIELDS = frozenset({
    "hostid", "state", "visible", "passworded", "maxplayers",
    "matchtype", "isObservable", "observerDelay",
})


def _parse_json_list(raw: Any, default: str = "[]") -> list:
    if isinstance(raw, list):
        return raw
    return json.loads(raw if raw is not None else default)


def _coerce_int(value: Any) -> Any:
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


class MatchmakingManager:
    def __init__(self, initial_match_id: int = INITIAL_MATCH_ID):
        self.advertisements: list[dict] = []
        self.last_match_id = initial_match_id

    def get_advertisement(self, advertisement_id: int) -> dict:
        logger.debug(f"Getting advertisement with ID: {advertisement_id}")
        advertisement = self._find_advertisement(advertisement_id)
        if advertisement is None:
            logger.error(f"Advertisement ID: {advertisement_id} not found.")
            return {}
        return advertisement

    def create_advertisement(self, params: dict) -> dict:
        self.last_match_id += 1
        new_id = self.last_match_id
        now = time.time()

        advertisement = {
            "advertisementid": new_id,
            "platformLobbyID": None,
            "unknown": "0",
            "hostid": int(params["hostid"]),
            "state": int(params["state"]),
            "description": params["description"],
            "visible": int(params["visible"]),
            "mapname": params["mapname"],
            "options": params["options"],
            "passworded": int(params["passworded"]),
            "maxplayers": int(params["maxplayers"]),
            "slotinfo": params["slotinfo"],
            "matchtype": int(params["matchtype"]),
            "peers": [],
            "unk": 0,
            "unk1": 512,
            "isObservable": int(params["isObservable"]),
            "observerDelay": int(params["observerDelay"]),
            "unk4": 0,
            "unk5": 0,
            "startGameTime": None,
            "relayRegion": params["relayRegion"],
            "endGameTime": None,
            "createdAt": now,
        }
        logger.debug(advertisement)
        self.advertisements.append(advertisement)
        return advertisement

    def update_advertisement(self, params: dict) -> dict | None:
        advertisement_id = params.get("advertisementid")
        if advertisement_id is None:
            logger.error("UpdateAdvertisement: advertisementid is required")
            return None

        advertisement = self.get_advertisement(int(advertisement_id))
        if not advertisement:
            logger.error(f"UpdateAdvertisement: advertisement {advertisement_id} not found")
            return None

        for key in _UPDATE_FIELDS:
            if key not in params:
                continue
            value = params[key]
            if key in _INT_UPDATE_FIELDS:
                value = _coerce_int(value)
            advertisement[key] = value

        logger.debug(f"Updated advertisement {advertisement_id}: {advertisement}")
        return advertisement

    def add_peer(self, params: dict) -> None:
        match_id = int(params["match_id"])
        advertisement = self.get_advertisement(match_id)
        if not advertisement:
            logger.error(f"Advertisement {match_id} not found")
            return

        profile_ids = _parse_json_list(params["profile_ids"])
        race_ids = _parse_json_list(params["race_ids"])
        stat_group_ids = _parse_json_list(params["statGroup_ids"])
        team_ids = _parse_json_list(params["teamIDs"])

        logger.debug(
            f"Parsed lists: profiles={profile_ids}, races={race_ids}, "
            f"statGroups={stat_group_ids}, teams={team_ids}"
        )

        for profile_id, race_id, stat_group_id, team_id in zip(
            profile_ids, race_ids, stat_group_ids, team_ids
        ):
            self._add_or_update_peer(
                advertisement,
                match_id,
                int(profile_id),
                int(stat_group_id),
                int(race_id),
                int(team_id),
            )

        logger.debug(f"Advertisement after AddPeer: {advertisement}")

    def peer_update(self, params: dict) -> bool:
        match_id_str = params.get("match_id")
        if not match_id_str:
            logger.error("PeerUpdate: match_id is required")
            return False

        match_id = int(match_id_str)
        advertisement = self.get_advertisement(match_id)
        if not advertisement:
            logger.error(f"PeerUpdate: Advertisement {match_id} not found")
            return False

        try:
            profile_ids = _parse_json_list(params.get("profile_ids"))
            race_ids = _parse_json_list(params.get("race_ids"))
            team_ids = _parse_json_list(params.get("teamIDs"))
            is_non_participants = _parse_json_list(params.get("isNonParticipants"))
        except json.JSONDecodeError:
            logger.error("PeerUpdate: Failed to decode JSON params")
            return False

        logger.debug(
            f"PeerUpdate params parsed for Match {match_id}: "
            f"Profiles={profile_ids}, Races={race_ids}"
        )

        for index, profile_id in enumerate(profile_ids):
            peer = self._find_peer(advertisement, int(profile_id))
            if peer is None:
                logger.warning(
                    f"PeerUpdate: Peer {profile_id} not found in lobby {match_id}, skipping."
                )
                continue

            if index < len(race_ids):
                peer["raceID"] = int(race_ids[index])
            if index < len(team_ids):
                peer["team"] = int(team_ids[index])
            if index < len(is_non_participants) and int(is_non_participants[index]) == 1:
                logger.debug(f"Peer {profile_id} marked as non-participant (observer)")

        logger.debug(f"Updated advertisement {match_id} peers: {advertisement['peers']}")
        return True

    def remove_peer(self, advertisement_id: int, profile_id: int) -> bool:
        advertisement = self._find_advertisement(advertisement_id)
        if advertisement is None:
            return False

        initial_peer_count = len(advertisement["peers"])
        advertisement["peers"] = [
            peer for peer in advertisement["peers"]
            if peer["profileID"] != int(profile_id)
        ]
        return len(advertisement["peers"]) < initial_peer_count

    def cleanup_empty_advertisements(
        self,
        referenced_ids: set[int],
        grace_seconds: float,
    ) -> list[int]:
        now = time.time()
        deleted_ids: list[int] = []

        for advertisement in list(self.advertisements):
            if advertisement["peers"]:
                continue

            advertisement_id = advertisement["advertisementid"]
            if advertisement_id in referenced_ids:
                continue

            created_at = advertisement.get("createdAt", now)
            if now - created_at < grace_seconds:
                continue

            if self.delete_advertisement(advertisement_id):
                deleted_ids.append(advertisement_id)

        return deleted_ids

    def delete_advertisement(self, advertisement_id: int) -> bool:
        advertisement = self._find_advertisement(advertisement_id)
        if advertisement is None:
            logger.error(f"DeleteAdvertisement: Lobby {advertisement_id} not found.")
            return False

        logger.info(
            f"Deleting lobby {advertisement_id}. Host: {advertisement.get('hostid')}"
        )
        self.advertisements.remove(advertisement)
        logger.debug(f"Lobby {advertisement_id} successfully deleted.")
        return True

    def _find_advertisement(self, advertisement_id: int) -> dict | None:
        for advertisement in self.advertisements:
            if advertisement["advertisementid"] == advertisement_id:
                return advertisement
        return None

    def _find_peer(self, advertisement: dict, profile_id: int) -> dict | None:
        for peer in advertisement["peers"]:
            if peer["profileID"] == profile_id:
                return peer
        return None

    def _add_or_update_peer(
        self,
        advertisement: dict,
        match_id: int,
        profile_id: int,
        stat_group_id: int,
        race_id: int,
        team_id: int,
    ) -> None:
        existing_peer = self._find_peer(advertisement, profile_id)
        if existing_peer:
            logger.debug(
                f"Peer {profile_id} already exists in lobby {match_id}. Updating/Skipping."
            )
            existing_peer["raceID"] = race_id
            existing_peer["team"] = team_id
            return

        peer = {
            "advertisementID": match_id,
            "profileID": profile_id,
            "party": -1,
            "statGroupID": stat_group_id,
            "raceID": race_id,
            "team": team_id,
            "route": DEFAULT_ROUTE,
        }
        advertisement["peers"].append(peer)
        logger.debug(f"Added peer: {peer}")


_manager = MatchmakingManager()

advertisements = _manager.advertisements
lastMatchID = _manager.last_match_id


async def GetAdvertisement(advertisementID: int):
    return _manager.get_advertisement(advertisementID)


async def CreateAdvertisement(params: dict):
    global lastMatchID
    advertisement = _manager.create_advertisement(params)
    lastMatchID = _manager.last_match_id
    return advertisement


async def UpdateAdvertisement(params: dict):
    return _manager.update_advertisement(params)


async def AddPeer(params: dict):
    _manager.add_peer(params)


async def PeerUpdate(params: dict):
    return _manager.peer_update(params)


async def DeleteAdvertisement(advertisementID: int):
    return _manager.delete_advertisement(advertisementID)


def RemovePeerFromAdvertisement(advertisement_id: int, profile_id: int) -> bool:
    return _manager.remove_peer(advertisement_id, profile_id)


def CleanupEmptyAdvertisements(
    referenced_ids: set[int],
    grace_seconds: float,
) -> list[int]:
    return _manager.cleanup_empty_advertisements(referenced_ids, grace_seconds)