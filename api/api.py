from fastapi import FastAPI, Response
import uvicorn
import json
from time import sleep

from api.utils.datautils import read_datafile, relicjson
from api.core import auth, sessions, responses, chat, inventory, game_session

from api.database.scripts import create_account
from api.database.interract import get_userdata

from api.protocols.game.advertisement.peerAdd import advertisements_peerAdd

api = FastAPI()

@api.post('/game/login/platformlogin')
async def game_login_platformlogin(platformUserID, alias):
    account_data = get_userdata(steamid=platformUserID)
    print(account_data)
    
    if account_data is None:
        try:
            auth.steam_create(steamid=platformUserID)
            account_data = get_userdata(steamid=platformUserID)
        except Exception as e:
            print(f"error: {e}")
            return Response(status_code=500)

    if account_data is not None:
        data = auth.steam_auth(platformUserID, alias)
        resp = relicjson(data)
        return Response(content=resp)
    else:
        return Response(status_code=404)


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
async def game_Achievement_getAvailableAchievements():
    resp = f'[0,[],"comrade_signature"]'
    return Response(content=resp)


@api.get('/game/account/getProfileName')
async def game_account_getProfileName(sessionID):
    resp = responses.data_getProfileName(sessionID=sessionID)
    print(resp)
    return Response(content=resp)
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
async def game_item_getItemDefinitionsJson():
    data = {"result": 0, "dataSignature": "comrade_signature"}
    resp = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return Response(content=resp)
@api.get('/game/item/getItemBundleItemsJson')
async def game_item_getItemBundleItemsJson():
    resp = json.dumps(itemBundleItems, separators=(",", ":"), ensure_ascii=False)
    #print(resp)
    return Response(content=resp)


@api.get('/game/item/getInventoryByProfileIDs')
async def game_item_getInventoryByProfileIDs(profileIDs):
    id = str(profileIDs[1])
    print(id)
    resp = inventory.fetch_inventory_data(profileID=id)
    print(resp)
    return Response(content=resp)
@api.post('/game/item/moveItem')
async def game_item_moveItem(sessionID, posIDs, itemIDs, itemLocationIDs):
    print(f"posIDs:{posIDs} itemIDs:{itemIDs}, itemLocationIDs:{itemLocationIDs}")
    resp = inventory.moveItem(posIDs=posIDs,
                              itemIDs=itemIDs,
                              itemLocationIDs=itemLocationIDs,
                              sessionID=sessionID)
    print(resp)
    return Response(content=str(resp))


# matchmaking (advertisements)
# it's a sequence of requests and responses
# when hosting, game requests are: /game/advertisement/host -> /game/advertisement/peerAdd -> /game/advertisement/updatePlatformLobbyID -> /game/login/readSession
@api.post('/game/advertisement/host')
async def game_advertisement_host(sessionID, hostid, relayRegion, party, race, team):
    resp = game_session.create_lobby(sessionID=sessionID, hostid=hostid, relayRegion=relayRegion, party=party, race=race, team=team)
    return Response(content=relicjson(resp))
@api.post('/game/party/peerAdd')
async def game_advertisement_peerAdd():
    resp = advertisements_peerAdd()
    return Response(content=relicjson(resp))
@api.post('/game/advertisement/updatePlatformLobbyID')
def game_advertisement_updatePlatformLobbyID(sessionID, platformlobbyID):
    resp = game_session.update_session_PlatformLobbyID(sessionID=sessionID, platformLobbyID=platformlobbyID)
    return Response(content=relicjson(resp))
@api.post('/game/advertisement/update')
def game_advertisement_update():
    resp = game_session.update_lobby()
    return Response(content=relicjson(resp))

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