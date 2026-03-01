import json
from dataclasses import dataclass, astuple

import time

from common.logger import logger

from managers import matchmaking

@dataclass
class response:
    result: int

async def Handle(params: dict):
    updated = await matchmaking.UpdateAdvertisement(params)
    
    result = None
    
    if updated is None:
        logger.warning("Update advertisement failed or not found")
        result = response(result=1)
    
    result = response(result=0)
    
    # must sleep here. if server will send response too fast the game will bug
    time.sleep(2)
    
    return json.dumps(result, separators=(",",";"), default=astuple)
