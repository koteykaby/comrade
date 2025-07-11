from fastapi import FastAPI, Response
import uvicorn
import json
from time import sleep

from api.utils.datautils import read_datafile, relicjson
from api.core import auth, sessions, responses, chat, inventory, game_session, matchmaking

from api.database.scripts.change_username import change_username
from api.database.interract import get_userdata

from api.protocols.game.advertisement.peerAdd import advertisements_peerAdd
from api.protocols.game.advertisement.updateState import advertisement_updateState
from api.protocols.game.advertisement.update import advertisement_update

api = FastAPI()

@api.post('/game/login/platformlogin')
async def game_login_platformlogin(platformUserID, alias):
    account_data = get_userdata(steamid=platformUserID)
    
    if account_data is None:
        try:
            auth.steam_create(steamid=platformUserID, username=alias)
            account_data = get_userdata(steamid=platformUserID)
        except Exception as e:
            print(f"error: {e}")
            return Response(status_code=500)

    if account_data is not None:
        if account_data.data['profile_info']['alias'] != str(alias):
            change_username(id=account_data.id, username=alias)
        data = auth.steam_auth(platformUserID, alias)
        resp = relicjson(data)
        return Response(content=resp)
    else:
        return Response(status_code=404)


@api.post('/game/login/readSession')
async def game_login_readSession(sessionID, ack):
    data = await sessions.client_readSession_handle(sessionID=str(sessionID), ack=int(ack))
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
async def game_account_getProfileName(profile_ids):
    resp = responses.data_getProfileName(profile_ids=json.loads(profile_ids))
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
@api.post('/game/account/FindProfilesByPlatformID')
async def game_account_FindProfilesByPlatformID(platformIDs):
    resp = relicjson(responses.players_FindProfilesByPlatformID(platformIDs=list(platformIDs)))
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
@api.post('/game/item/signItems')
async def game_item_signItems():
    # signature packet template:
    # [
    #    0,
    #    "comrade_signature" // signature
    # ]
    # original sig is base64 encoded (and encrypted?), i'll try to put my own like i did before
    # in the other sigs handling request handling
    resp = '[0,"comrade_signature"]'
    return Response(content=resp)

@api.get('/game/item/getInventoryByProfileIDs')
async def game_item_getInventoryByProfileIDs(profileIDs):
    id = str(profileIDs[1])
    resp = inventory.fetch_inventory_data(profileID=id)
    return Response(content=resp)
@api.post('/game/item/moveItem')
async def game_item_moveItem(sessionID, itemIDs, itemLocationIDs):
    print(f"itemIDs:{itemIDs}, itemLocationIDs:{itemLocationIDs}")    
    resp = inventory.moveItems(sessionID=sessionID,
                               itemIDs=itemIDs,
                               itemLocationIDs=itemLocationIDs)
    print(relicjson(resp))
    return Response(content=relicjson(resp))
@api.get('/game/item/getItemLoadouts')
async def game_item_getItemLoadouts():
    resp = "[0,[]]"
    return Response(content=resp)

# statistics
@api.post('/game/Leaderboard/getRecentMatchHistory')
async def game_Leaderboard_getRecentMatchHistory():
    resp = "[0,[]]" # TODO
    return Response(content=resp)
@api.post('/game/Challenge/getChallengeProgress')
async def game_Challenge_getChallengeProgress():
    resp = "[0,[]]" # TODO
    return Response(content=resp)
@api.get('/game/Leaderboard/getStatGroupsByProfileIDs')
async def game_Leaderboard_getStatGroupsByProfileIDs(profileids, sessionID):
    resp = responses.data_getStatGroupsByProfileIDs(ids=list(profileids), sessionID=sessionID)
    return Response(content=relicjson(resp))
@api.get('/game/Leaderboard/getPersonalStat')
async def game_Leaderboard_getPersonalStat():
    resp = '[0]' # TODO
    return Response(content=resp)
@api.get('/game/Achievement/getAchievements')
async def game_Achievement_getAchievements(profileIDs):
    id = list(profileIDs)
    resp = f'[0,[[{id[1]},[]]]]'
    return Response(content=resp)

# matchmaking (advertisements)
# it's a sequence of requests and responses
# when hosting, game requests are: /game/advertisement/host -> /game/advertisement/peerAdd -> /game/advertisement/updatePlatformLobbyID -> /game/login/readSession
@api.post('/game/advertisement/host')
async def game_advertisement_host(sessionID, 
                                  hostid, 
                                  visible,
                                  mapname, 
                                  options, 
                                  slotinfo,
                                  maxplayers, 
                                  matchtype, 
                                  relayRegion, 
                                  party, 
                                  race, 
                                  team, 
                                  isObservable,
                                  observerDelay,
                                  passworded):
    resp = game_session.init_game_session(sessionID=str(sessionID),
                                          hostid=int(hostid), 
                                          visible=int(visible),
                                          mapname=str(mapname), 
                                          options=str(options), 
                                          slotinfo=str(slotinfo),
                                          passworded=int(passworded), 
                                          maxplayers=int(maxplayers), 
                                          matchType=int(matchtype), 
                                          relayRegion=str(relayRegion), 
                                          party=int(party), 
                                          race=int(race), 
                                          team=int(team),
                                          isObservable=int(isObservable),
                                          observerDelay=int(observerDelay))
    return Response(content=relicjson(resp))
@api.post('/game/advertisement/updatePlatformLobbyID')
async def game_advertisement_updatePlatformLobbyID(sessionID, matchID, platformlobbyID):
    resp = game_session.update_session_PlatformLobbyID(sessionID=sessionID, lobby_id=matchID, platformLobbyID=platformlobbyID)
    return Response(content=relicjson(resp))
@api.post('/game/advertisement/update')
async def game_advertisement_update(advertisementid,
                                    description,
                                    mapname,
                                    visible,
                                    isObservable,
                                    matchtype,
                                    maxplayers,
                                    observerDelay,
                                    options,
                                    passworded,
                                    slotinfo,
                                    state):
    game_session.update_lobby(advertisementid=int(advertisementid),
                              description=str(description),
                              mapname=str(mapname),
                              visible=int(visible),
                              isObservable=int(isObservable),
                              matchType=int(matchtype),
                              maxplayers=int(maxplayers),
                              observerDelay=int(observerDelay),
                              options=str(options),
                              passworded=int(passworded),
                              slotinfo=str(slotinfo),
                              state=int(state))
    resp = advertisement_update()
    return Response(content=relicjson(resp))
@api.post('/game/advertisement/updateState')
async def game_advertisement_updateState():
    resp = advertisement_updateState()
    return Response(content=relicjson(resp))

@api.post('/game/advertisement/leave')
async def game_advertisement_leave(sessionID, advertisementid):
    resp = game_session.leave.advertisement_leave()
    game_session.peer_leave(sessionID=sessionID, advertisementID=int(advertisementid))
    return Response(content=relicjson(resp))

# party operations
@api.post('/game/party/peerAdd')
async def game_advertisement_peerAdd(match_id, profile_ids, race_ids, teamIDs):
    resp = advertisements_peerAdd()
    game_session.add_peer(match_id=int(match_id),
                          profile_ids=json.loads(profile_ids),
                          raceIDs=json.loads(race_ids),
                          teamIDs=json.loads(teamIDs))
    return Response(content=relicjson(resp))
@api.post('/game/party/updateHost')
async def game_advertisement_updateHost(sessionID, match_id):
    resp = game_session.update_Host(sessionID=str(sessionID),
                                    advertisementID=int(match_id))
    return Response(content=resp)
@api.post('/game/party/sendMatchChat')
async def game_party_sendMatchChat(match_id,message,messageTypeID,from_profile_id,to_profile_id,broadcast):
    resp = chat.chat_sendMatchChat()
    print(f'[SendMatchChat] Player {from_profile_id} in {match_id} sent to {to_profile_id} \nMessage: {message}\nmessageTypeID:{messageTypeID} is broadcast: {broadcast}')
    return Response(content=relicjson(resp))


# lobby operations are completed, so lets show lobbies for the browser!
@api.post('/game/advertisement/findAdvertisements')
async def game_advertisement_findAdvertisements():
    resp = matchmaking.discover()
    print(relicjson(resp))
    return Response(content=relicjson(resp))

# connecting to the new lobby
# sequence again 
# GET /game/advertisement/getAdvertisements -> POST /game/advertisement/join
@api.get('/game/advertisement/getAdvertisements')
async def game_advertisement_getAdvertisements(match_ids: str):  
    cleaned_ids = match_ids.strip("[]").split(",")
    # clearing
    match_ids_list = [int(match_id) for match_id in cleaned_ids if match_id.strip()]
    
    data = matchmaking.get_advertisements(matchIDs=match_ids_list)  
    resp = data[0] if isinstance(data, list) and len(data) == 1 else data
    print(f'requested adv: {relicjson(resp)}')
    return Response(content=relicjson(resp))
@api.post('/game/advertisement/join')
async def game_advertisement_join(advertisementid, sessionID, party, race, team):
    print(f'JOINING SESSION: adv:{advertisementid} session {sessionID}')
    resp = matchmaking.join_lobby(sessionID=sessionID,
                                  advID=advertisementid,
                                  party=party,
                                  raceID=race,
                                  teamID=team)
    print(relicjson(resp))
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
                port=cfg_a['port'],
                ssl_certfile='ssl/certificate.pem',
                ssl_keyfile='ssl/private_key.pem')