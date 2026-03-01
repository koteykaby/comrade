import asyncio
import json
from dataclasses import dataclass, astuple
from time import time

from common.logger import logger

from managers.sessions import GetSession, GetSessionByProfileID
from managers.account import GetAccount
from managers.matchmaking import GetAdvertisement

from models.user import profilePresenceInfo

from models.advertisements import Advertisement, Peer 

@dataclass
class response:
    notifications: list

@dataclass
class PresenceMessage:
    result: int
    description: str
    profileID: int
    profilePresences: list[profilePresenceInfo]
    
@dataclass
class ExtensionMessage:
    result: int
    description: str
    data: list 
    
@dataclass
class PlatformSessionUpdateMessage:
    result: int
    description: str
    profileID: int
    data: list

@dataclass
class MatchStartMessage:
    result: int
    description: str
    profileID: int
    data: list

async def Handle(sessionID: str, timeout: int = 30):
    sessionData = GetSession(sessionID)

    notifications = []
    end_time = asyncio.get_event_loop().time() + timeout

    while not notifications:
        if sessionData["notifications"]:
            notif = sessionData["notifications"].popleft()
            sessionData["ack"] += 1
            
            userData = GetAccount(sessionData["platformUserID"])
            current_profile_id = userData["profileInfo"]["id"]

            if notif == "PresenceMessage":
                presenceMsg = PresenceMessage(
                    result=0,
                    description="PresenceMessage",
                    profileID=current_profile_id,
                    profilePresences=[
                        profilePresenceInfo(
                            **userData["profileInfo"],
                            presenceID=1,
                            presenceLocalized=None,
                            presenceProperty=[]
                        )
                    ]
                )
                notifications.append(astuple(presenceMsg))

            elif notif == "ExtensionMessage":
                extensionMsg = ExtensionMessage(
                    result=0,
                    description="ExtensionMessage",
                    data=[0, str(userData["characterData"])]
                )
                notifications.append(astuple(extensionMsg))
                
            elif notif == "PlatformSessionUpdateMessage":
                adv_ref = sessionData.get("advertisement")
                if adv_ref:
                     adv = await GetAdvertisement(adv_ref["id"])
                else:
                     adv = None

                platformSessionUpdateMsg = PlatformSessionUpdateMessage(
                    result=0,
                    description="PlatformSessionUpdateMessage",
                    profileID=current_profile_id,
                    data=[
                        adv["advertisementid"] if adv else 0,
                        "0",
                        adv["platformLobbyID"] if adv else 0,
                    ]
                )
                notifications.append(astuple(platformSessionUpdateMsg))

            elif notif == "MatchStartMessage":
                adv_ref = sessionData.get("advertisement")
                if not adv_ref:
                    logger.error(f"MatchStartMessage: No advertisement found for session {sessionID}")
                    continue
                
                raw_adv = await GetAdvertisement(adv_ref["id"])
                if not raw_adv:
                    logger.error(f"MatchStartMessage: Advertisement {adv_ref['id']} not found")
                    continue

                peers_list = raw_adv.get("peers", [])
                
                unk_values_list = []
                peer_indices_list = []
                inventory_list = []
                unk_end_list = []

                for idx, peer in enumerate(peers_list):
                    p_id = peer["profileID"]
                    s = GetSessionByProfileID(p_id)
                    str_p_id = str(p_id)
                    
                    # those values repeats all the time
                    unk_values_list.append([
                        p_id, 
                        [231430, 231451, 317850] 
                    ])
                    
                    peer_indices_list.append([
                        str_p_id,
                        str(idx) # trying to use peer index as peer id
                    ])
                    
                    inventory_list.append([
                        str_p_id,
                        s['equipedItems']
                    ])
                    
                    unk_end_list.append([
                        str_p_id,
                        [] 
                    ])

                adv_model = Advertisement(
                    **{k: v for k, v in raw_adv.items() if k != "peers"},
                    peers=[Peer(**p) for p in peers_list]
                )
                
                adv_tuple = astuple(adv_model)

                match_start_data = [
                    unk_values_list,
                    peer_indices_list,
                    int(time()),
                    inventory_list,
                    adv_tuple,
                    unk_end_list
                ]

                msg = MatchStartMessage(
                    result=0,
                    description="MatchStartMessage",
                    profileID=current_profile_id,
                    data=match_start_data
                )
                
                logger.info(f"Sending MatchStartMessage to {current_profile_id}")
                
                logger.debug(msg)
                
                notifications.append(astuple(msg))

        else:
            now = asyncio.get_event_loop().time()
            if now >= end_time:
                break
            await asyncio.sleep(0.5)

    if not notifications:
        return f"{sessionData['ack']},[[]]"

    notificationsList = response(notifications)
    
    result = f"{sessionData['ack']},{json.dumps(notificationsList, separators=(',', ':'), default=astuple)}"
    
    return result