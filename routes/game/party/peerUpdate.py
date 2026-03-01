from common.logger import logger

from managers import matchmaking

async def Handle(params: dict):
    await matchmaking.PeerUpdate(params)
    return [0]