from dataclasses import dataclass, astuple
import json

from common.logger import logger
from models.advertisements import Advertisement, Peer
from managers.matchmaking import advertisements

@dataclass
class response:
    result: int
    advs: list[Advertisement]

async def Handle(match_ids):
    advIDs = json.loads(match_ids)
    
    logger.debug(f"Getting advertisements {advIDs}")
    
    filtered_advs = [
        Advertisement(
            **{k: v for k, v in adv.items() if k != "peers"},
            peers=[Peer(**p) for p in adv["peers"]],
        )
        for adv in advertisements
        if adv.get("advertisementid") in advIDs
    ]

    result = response(
        result=0,
        advs=filtered_advs
    )
    
    logger.debug(f"getAdvertisement result: {result}")
    
    return json.dumps(result, separators=(",", ":"), default=astuple)