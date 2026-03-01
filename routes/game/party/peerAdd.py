from managers.matchmaking import AddPeer

async def Handle(params):
    await AddPeer(params)
    return [0]