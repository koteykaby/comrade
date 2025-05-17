from fastapi import FastAPI, Response
import uvicorn
import json
from time import sleep

from api.core.utils.datautils import read_datafile, relicjson
from api.core import auth, sessions, inventory, responses, chat

api = FastAPI()

@api.post('/game/login/platformlogin')
async def game_login_platformlogin(platformUserID, alias):
    try:
        data = auth.steam_auth(platformUserID, alias)
    except AttributeError:
        auth.steam_create(steamid=platformUserID)
    finally:
        data = auth.steam_auth(platformUserID, alias)
    resp = relicjson(data)
    return Response(content=resp)
@api.post('/game/login/readSession')
async def game_login_readSession(sessionID, ack):
    data = sessions.client_readSession_handle(sessionID=sessionID, ack=int(ack))
    resp = data
    return Response(content=resp)
@api.post('/game/login/logout')
async def game_login_logout(sessionID):
    sessions.client_sessionClear(sessionID)

@api.get('/game/news/getNews')
async def game_news_getNews():
    resp = '[0,[],[]]'
    return Response(content=resp)
@api.get('/game/automatch/getAutomatchMap')
async def game_automatch_getAutomatchMap():
    return Response(content=automatch_maps_list)

@api.get('/game/Achievement/getAvailableAchievements')
async def game_Achievement_getAvailableAchievements(signature):
    resp = f'[0,[],"{str(signature)}"]'
    return Response(content=resp)

@api.get('/game/account/getProfileName')
async def game_account_getProfileName(sessionID):
    resp = responses.data_getProfileName(sessionID=sessionID)
    return Response(resp)
@api.post('/game/chat/getChatChannels')
async def game_chat_getChatChannels():
    resp = "[0,[],100]"
    return Response(content=resp)
@api.get('/game/chat/getOfflineMessages')
async def game_chat_getOfflineMessages(sessionID):
    resp = chat.resp_getOfflineMessages(sessionID=sessionID)
    return Response(content=resp)

@api.post('/game/relationship/setPresenceProperty')
async def game_relationship_setPresenceProperty():
    resp = "[0]"
    return Response(content=resp)
@api.post('/game/account/setCrossplayEnabled')
async def game_account_setCrossplayEnabled():
    resp = "[0]"
    return Response(content=resp)

@api.get('/game/Leaderboard/getAvailableLeaderboards')
async def game_Leaderboard_getAvailableLeaderboards():
    resp = available_leaderboards_list
    return Response(content=resp)

@api.post('/game/item/getItemPrices')
async def game_item_getItemPrices():
    resp = item_prices
    return Response(content=resp)
@api.get('/game/item/getScheduledSaleAndItems')
async def game_item_getScheduledSaleAndItems():
    resp = '[0,[],[],2927]'
    return Response(content=resp)
@api.post('/game/item/getPersonalizedSaleItems')
async def game_item_getPersonalizedSaleItems():
    resp = PersonalizedSaleItems
    return Response(content=resp)
@api.get('/game/item/getItemDefinitionsJson')
async def game_item_getItemDefinitionsJson(signature):
    data = {"result": 0, "dataSignature": str(signature)}
    resp = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return Response(content=resp)
@api.get('/game/item/getItemBundleItemsJson')
async def game_item_getItemBundleItemsJson():
    resp = json.dumps(itemBundleItems, separators=(",", ":"), ensure_ascii=False)
    #print(resp)
    return Response(content=resp)

if __name__ == "__main__": 
    itemBundleItems = json.load(open('data/itemBundleItems.json', 'r'))
    PersonalizedSaleItems = read_datafile('data/PersonalizedSaleItems.json')
    item_prices = read_datafile('data/itemPrices.json')
    automatch_maps_list = read_datafile('data/automatchMap.json')
    available_leaderboards_list = read_datafile('data/availableLeaderboards.json')
    values = json.load(open('data/values.json', 'r'))
    cfg = json.load(open('config/config.json', 'r'))
    cfg_a = cfg['api']
    
    uvicorn.run(app=api,
                host=cfg_a['address'],
                port=443,
                ssl_certfile='ssl/certificate.pem',
                ssl_keyfile='ssl/private_key.pem')