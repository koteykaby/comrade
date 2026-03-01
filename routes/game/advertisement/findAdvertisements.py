from dataclasses import dataclass, astuple
import json

from common.logger import logger

from models.advertisements import Advertisement, Peer

from managers.matchmaking import advertisements

@dataclass
class response:
    result: int
    advs: list[Advertisement]
    end: list

async def Handle():
    result = response(
        result=0,
        advs=[
            Advertisement(
                **{k: v for k, v in adv.items() if k != "peers"},
                peers=[Peer(**p) for p in adv["peers"]],
            )
            for adv in advertisements
        ],
        end=[]
    )
    
    logger.debug(f"FindAdvertisements result: {result}")
    
    return json.dumps(result, separators=(",", ":"), default=astuple)