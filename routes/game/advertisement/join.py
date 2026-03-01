from dataclasses import dataclass, astuple
import json

from singletons import servicesConfig

from common.logger import logger

from models.advertisements import Peer

from managers import sessions, account, matchmaking

@dataclass
class response:
    result: int
    route: str
    ipv4: str
    bsPort: int
    webSocketPort: int
    outOfBandPort: int
    peers: list[Peer]

async def Handle(sessionID, advertisementid, party, race, team):
    logger.debug(f"Calling join with sessionID: {sessionID}, advertisementID: {advertisementid}")
    
    sessionData = sessions.GetSession(sessionID)
    userData = account.GetAccount(sessionData["platformUserID"])
    advertisement = await matchmaking.GetAdvertisement(int(advertisementid))
    
    sessions.AddToAdvertisement(sessionID, int(advertisementid))
    
    peerInfo = Peer(
        int(advertisementid),
        profileID=userData["profileInfo"]["id"],
        party=int(party),
        statGroupID=userData["profileInfo"]["personalStatGroupID"],
        raceID=int(race),
        team=int(team),
        route="/10.0.7.136"
    )
    
    battleserverInfo = dict()
    
    for i in servicesConfig["battleservers"]:
        if i["region"] == advertisement["relayRegion"]:
            battleserverInfo = i
        else:
            battleserverInfo = servicesConfig["battleservers"][0]
    
    result = response(
        result=0,
        route="/10.0.7.136",
        ipv4=battleserverInfo["address"],
        bsPort=battleserverInfo["ports"]["bs_port"],
        webSocketPort=battleserverInfo["ports"]["websocket_port"],
        outOfBandPort=battleserverInfo["ports"]["out_of_band_port"],
        peers=[peerInfo]
    )
    
    return json.dumps(result, separators=(",",";"), default=astuple)