from fastapi import FastAPI, Request, Response, params
import uvicorn

from singletons import servicesConfig

from common.logger import logger

from routes.game.login import platformlogin, readSession, logout
from routes.game.news import getNews
from routes.game.automatch import getAutomatchMap
from routes.game.Achievement import getAchievements, getAvailableAchievements
from routes.game._achievement import syncStats
from routes.game.Challenge import getChallengeProgress
from routes.game.item import getItemDefinitionsJson, getItemBundleItemsJson, signItems, getInventoryByProfileIDs, getItemLoadouts, moveItem
from routes.game.Leaderboard import getAvailableLeaderboards, getRecentMatchHistory, getStatGroupsByProfileIDs
from routes.game.chat import getChatChannels, getOfflineMessages
from routes.game.relationship import setPresenceProperty
from routes.game.account import getProfileName, setCrossplayEnabled, FindProfilesByPlatformID
from routes.game.advertisement import host, updatePlatformLobbyID, update, findAdvertisements, getAdvertisements, join, leave, updateState
from routes.game.party import peerAdd, peerUpdate

from managers.matchmaking import advertisements
from managers.sessions import sessions

api = FastAPI()

# Endpoints for debugging
@api.get("/debug/findAdvertisements")
async def debug_findAdvertisements():
    return advertisements
@api.get("/debug/forceChangeState")
async def debug_forceChangeState(id, state):
    await updateState.Handle(id, state)
    return "CHANGED!"
@api.get("/debug/sessions")
async def debug_sessions():
    return sessions

@api.post("/game/login/platformlogin")
async def game_login_platformlogin(platformUserID, alias): return platformlogin.Handle(platformUserID, alias)
@api.post("/game/login/readSession")
async def game_login_readSession(sessionID): 
    result = await readSession.Handle(sessionID)
    return Response(content=result)
@api.post("/game/login/logout")
async def game_login_logout(sessionID): return await logout.Handle(sessionID)

@api.get("/game/automatch/getAutomatchMap")
async def game_automatch_getAutomatchMap(): return await getAutomatchMap.Handle()

@api.get("/game/news/getNews")
async def game_news_getNews(): return await getNews.Handle()

@api.get("/game/Achievement/getAvailableAchievements")
async def game_achievement_getAvailableAchievements(): 
    result = await getAvailableAchievements.Handle()
    return result
@api.post("/game/achievement/syncStats")
async def game_achievement_syncStats(): return await syncStats.Handle()
@api.get("/game/Achievement/getAchievements")
async def game_achievement_getAchievements(profileIDs): 
    result = await getAchievements.Handle(profileIDs)
    return Response(content=result)

@api.post("/game/Challenge/getChallengeProgress")
async def game_challenge_getChallengeProgress(): return await getChallengeProgress.Handle()

@api.get("/game/item/getItemDefinitionsJson")
async def game_item_getItemDefinitionsJson(): return await getItemDefinitionsJson.Handle()
@api.get("/game/item/getItemBundleItemsJson")
async def game_item_getItemBundleItemsJson(): return await getItemBundleItemsJson.Handle()
@api.post("/game/item/signItems")
async def game_item_signItems(): return await signItems.Handle()
@api.get("/game/item/getInventoryByProfileIDs")
async def game_item_getInventoryByProfileIDs(sessionID, profileIDs): 
    result = await getInventoryByProfileIDs.Handle(sessionID, profileIDs)
    return Response(content=result)
@api.get("/game/item/getItemLoadouts")
async def game_item_getItemLoadouts(): return await getItemLoadouts.Handle()

@api.post("/game/item/moveItem")
async def game_item_moveItem(sessionID, itemIDs, itemLocationIDs):
    result = await moveItem.Handle(sessionID, itemIDs, itemLocationIDs)
    return Response(content=result)

@api.get("/game/Leaderboard/getAvailableLeaderboards")
async def game_leaderboard_getAvailableLeaderboards(): return await getAvailableLeaderboards.Handle()

@api.get("/game/Leaderboard/getStatGroupsByProfileIDs")
async def game_leaderboard_getStatGroupsByProfileIDs(profileids):
    result = await getStatGroupsByProfileIDs.Handle(profileids)
    return Response(content=result)

@api.post("/game/Leaderboard/getRecentMatchHistory")
async def game_leaderboard_getRecentMatchHistory(): return await getRecentMatchHistory.Handle()

@api.post("/game/chat/getChatChannels")
async def game_chat_getChatChannels(): return await getChatChannels.Handle()
@api.get("/game/chat/getOfflineMessages")
async def game_chat_getOfflineMessages(sessionID): return await getOfflineMessages.Handle(sessionID)

@api.post("/game/account/setCrossplayEnabled")
async def game_account_setCrossplayEnabled(sessionID, crossplayEnabled):
    logger.debug(f"setCrossplayEnabled called with sessionID: {sessionID}, enabled: {crossplayEnabled}") 
    return await setCrossplayEnabled.Handle(sessionID, int(crossplayEnabled))
@api.get("/game/account/getProfileName")
async def game_account_getProfileName(profile_ids): 
    result = await getProfileName.Handle(profile_ids)
    return Response(content=result)
@api.post("/game/account/FindProfilesByPlatformID")
async def game_account_FindProfilesByPlatformID(platformIDs):
    logger.debug(f"FindProfilesByPlatformID called with platformUserIDs: {platformIDs}") 
    return await FindProfilesByPlatformID.Handle()

@api.post("/game/relationship/setPresenceProperty")
async def game_relationship_setPresenceProperty(sessionID, value):
    logger.debug(f"setPresenceProperty called with sessionID: {sessionID} with value: {value}") 
    return await setPresenceProperty.Handle()
@api.post("/game/relationship/getRelationships")
async def game_relationship_getRelationships():
    return [0,[],[],[],[],[],[],[]]

@api.post("/game/advertisement/host")
async def game_advertisement_host(request: Request): 
    params = dict(request.query_params)
    result = await host.Handle(params)
    return Response(content=result)
@api.post("/game/advertisement/updatePlatformLobbyID")
async def game_advertisement_updatePlatformLobbyID(sessionID, matchID, platformlobbyID):
    result = await updatePlatformLobbyID.Handle(sessionID, int(matchID), int(platformlobbyID))
    return result
@api.get("/game/advertisement/getAdvertisements")
async def game_advertisement_getAdvertisements(match_ids):
    result = await getAdvertisements.Handle(match_ids)
    return Response(content=result)
@api.post("/game/advertisement/findAdvertisements")
async def game_advertisement_findAdvertisements():
    result = await findAdvertisements.Handle()
    return Response(content=result)
@api.post("/game/advertisement/update")
async def game_advertisement_update(request: Request):
    params = dict(request.query_params)
    return await update.Handle(params)
@api.post("/game/advertisement/join")
async def game_advertisement_join(sessionID, advertisementid, party, race, team):
    result = await join.Handle(sessionID, advertisementid, party, race, team)
    return Response(content=result)
@api.post("/game/advertisement/leave")
async def game_advertisement_leave(sessionID, advertisementid):
    await leave.Handle(sessionID, int(advertisementid))
    return [0]
@api.post("/game/advertisement/updateState")
async def game_advertisement_updateState(advertisementid, state):
    await updateState.Handle(advertisementid, state)
    return [0]

@api.post("/game/party/peerAdd")
async def game_advertisement_peerAdd(request: Request):
    params = dict(request.query_params)
    return await peerAdd.Handle(params)
@api.post("/game/party/peerUpdate")
async def game_party_peerUpdate(request: Request):
    params = dict(request.query_params)
    return await peerUpdate.Handle(params)

if __name__ == "__main__":
    uvicorn.run(api, 
                host=servicesConfig["api"]["address"], 
                port=servicesConfig["api"]["port"], 
                reload=False,
                ssl_certfile=servicesConfig["ssl"]["cert"], 
                ssl_keyfile=servicesConfig["ssl"]["key"])