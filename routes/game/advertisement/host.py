import json
from dataclasses import astuple, dataclass

import time

from common.logger import logger
from singletons import servicesConfig

from managers import matchmaking
from managers import sessions
from managers import account

from models.advertisements import Peer

@dataclass
class response:
    result: int
    advID: int
    description: str
    ipv4: str
    bsPort: int
    webSocketPort: int
    outOfBandPort: int
    region: str
    peers: list
    unk: int
    unk1: str
    
async def Handle(params):
    sessionData = sessions.GetSession(params["sessionID"])
    userData = account.GetAccount(sessionData["platformUserID"])
    advertisement = await matchmaking.CreateAdvertisement(params)
    
    sessions.AddToAdvertisement(params["sessionID"], advertisement["advertisementid"])
    
    respPeer = Peer(
        advertisementID=advertisement["advertisementid"],
        profileID=advertisement["hostid"],
        party=int(params["party"]),
        statGroupID=userData["profileInfo"]["personalStatGroupID"],
        raceID=int(params["race"]),
        team=int(params["team"]),
        route="/10.0.7.136"
    )
    
    battleserverInfo = dict()
    
    for i in servicesConfig["battleservers"]:
        if i["region"] == advertisement["relayRegion"]:
            battleserverInfo = i
        else: 
            logger.warning(f"Couldn't load battleserver info for region {advertisement["relayRegion"]}, first one will be used")
            battleserverInfo = servicesConfig["battleservers"][0]
            
    logger.debug(f"Will be used battleserver: {battleserverInfo}")
    
    result = response(
        result=0,
        advID=advertisement["advertisementid"],
        description="authtoken",
        ipv4=battleserverInfo["address"],
        bsPort=battleserverInfo["ports"]["bs_port"],
        webSocketPort=battleserverInfo["ports"]["websocket_port"],
        outOfBandPort=battleserverInfo["ports"]["out_of_band_port"],
        region=advertisement["relayRegion"],
        peers=[list(astuple(respPeer))],
        unk=0,
        unk1="0"
    )
    
    logger.debug(f"Hosting result: {result}")
    
    # must sleep here. if server will send response too fast the game will bug
    time.sleep(2)
    
    return json.dumps(result, separators=(",",";"), default=astuple)