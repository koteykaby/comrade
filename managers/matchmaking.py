import json

from common.logger import logger

from managers import sessions

lastMatchID = 31005

advertisements = []

async def GetAdvertisement(advertisementID: int):
    logger.debug(f"Getting advertisement with ID: {advertisementID}")
    for adv in advertisements:
        if adv["advertisementid"] == advertisementID:
            #logger.debug(adv)
            return adv
    logger.error(f"Advertisement ID: {advertisementID} not found.")
    return dict()

async def CreateAdvertisement(params: dict):
    global advertisements, lastMatchID
    
    lastMatchID += 1
    newID = lastMatchID
    
    adv = {
        "advertisementid": newID,
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
        "endGameTime": None
    }
    
    logger.debug(adv)
    
    advertisements.append(adv)
    
    return adv
    
_UPDATE_FIELDS = (
    "hostid", "state", "description", "visible", "mapname", "options",
    "passworded", "maxplayers", "slotinfo", "matchtype",
    "isObservable", "observerDelay"
)

async def UpdateAdvertisement(params: dict):
    advertisement_id = params.get("advertisementid")
    if advertisement_id is None:
        logger.error("UpdateAdvertisement: advertisementid is required")
        return None

    advertisement = await GetAdvertisement(int(advertisement_id))
    if not advertisement:
        logger.error(f"UpdateAdvertisement: advertisement {advertisement_id} not found")
        return None

    for key in _UPDATE_FIELDS:
        if key not in params:
            continue
        value = params[key]
        if key in ("hostid", "state", "visible", "passworded", "maxplayers", "matchtype", "isObservable", "observerDelay"):
            try:
                value = int(value)
            except (TypeError, ValueError):
                pass
        
        advertisement[key] = value 

    logger.debug(f"Updated advertisement {advertisement_id}: {advertisement}")

    return advertisement

async def AddPeer(params: dict):
    match_id = int(params["match_id"])
    advertisement = await GetAdvertisement(match_id)
    
    if not advertisement:
        logger.error(f"Advertisement {match_id} not found")
        return

    profile_ids = json.loads(params["profile_ids"])
    race_ids = json.loads(params["race_ids"])
    statGroup_ids = json.loads(params["statGroup_ids"])
    teamIDs = json.loads(params["teamIDs"])

    logger.debug(
        f"Parsed lists: profiles={profile_ids}, races={race_ids}, "
        f"statGroups={statGroup_ids}, teams={teamIDs}"
    )

    for profile_id, race_id, stat_group_id, team_id in zip(
        profile_ids,
        race_ids,
        statGroup_ids,
        teamIDs
    ):
        p_id = int(profile_id)
        
        existing_peer = next((p for p in advertisement["peers"] if p["profileID"] == p_id), None)
        
        if existing_peer:
            logger.debug(f"Peer {p_id} already exists in lobby {match_id}. Updating/Skipping.")
            existing_peer["raceID"] = int(race_id)
            existing_peer["team"] = int(team_id)
            continue

        peer = {
            "advertisementID": match_id,
            "profileID": p_id,
            "party": -1,
            "statGroupID": int(stat_group_id),
            "raceID": int(race_id),
            "team": int(team_id),
            "route": "/10.0.7.136"
        }

        advertisement["peers"].append(peer)
        logger.debug(f"Added peer: {peer}")

    logger.debug(f"Advertisement after AddPeer: {advertisement}")
    
async def PeerUpdate(params: dict):
    match_id_str = params.get("match_id")
    if not match_id_str:
        logger.error("PeerUpdate: match_id is required")
        return False
        
    match_id = int(match_id_str)
    advertisement = await GetAdvertisement(match_id)
    
    if not advertisement:
        logger.error(f"PeerUpdate: Advertisement {match_id} not found")
        return False

    try:
        profile_ids = json.loads(params.get("profile_ids", "[]"))
        race_ids = json.loads(params.get("race_ids", "[]"))
        team_ids = json.loads(params.get("teamIDs", "[]"))
        is_non_participants = json.loads(params.get("isNonParticipants", "[]"))
    except json.JSONDecodeError:
        logger.error("PeerUpdate: Failed to decode JSON params")
        return False

    logger.debug(f"PeerUpdate params parsed for Match {match_id}: Profiles={profile_ids}, Races={race_ids}")

    for i, profile_id in enumerate(profile_ids):
        p_id = int(profile_id)
        
        peer = next((p for p in advertisement["peers"] if p["profileID"] == p_id), None)
        
        if not peer:
            logger.warning(f"PeerUpdate: Peer {p_id} not found in lobby {match_id}, skipping.")
            continue

        if i < len(race_ids):
            peer["raceID"] = int(race_ids[i])

        if i < len(team_ids):
            peer["team"] = int(team_ids[i])
            
        if i < len(is_non_participants):
            non_participant = int(is_non_participants[i])
            if non_participant == 1:
                logger.debug(f"Peer {p_id} marked as non-participant (observer)")

    logger.debug(f"Updated advertisement {match_id} peers: {advertisement['peers']}")
    return True
    
async def DeleteAdvertisement(advertisementID: int):
    global advertisements
    
    lobby_to_remove = None
    for adv in advertisements:
        if adv["advertisementid"] == advertisementID:
            lobby_to_remove = adv
            break
            
    if not lobby_to_remove:
        logger.error(f"DeleteAdvertisement: Lobby {advertisementID} not found.")
        return False
    
    logger.info(f"Deleting lobby {advertisementID}. Host: {lobby_to_remove.get('hostid')}")
    
    advertisements.remove(lobby_to_remove)
    
    logger.debug(f"Lobby {advertisementID} successfully deleted.")
    return True 