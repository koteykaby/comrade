import json
from dataclasses import dataclass, astuple
from managers import account
from models.user import profileInfo
from common.logger import logger

@dataclass
class unknownData:
    statgroupID: int
    clan: str # ??
    metadata: str # ??
    unkint: int ## ??
    profileIDs: list[int]
    # i just return ready datas

@dataclass
class response:
    result: int
    unknownList: list
    profileInfos: list
    leaderboardStats: list
    
async def Handle(profileids: str):
    pIDs = json.loads(profileids) # [243943, 439223, 438342]
    
    unknownList = list()
    profileInfosList = list()
    leaderboardStatsList = list()
    
    for pid in pIDs:
        userData = account.GetAccountByProfileID(int(pid))

        unknownList = [unknownData(
            statgroupID=userData["profileInfo"]["personalStatGroupID"],
            clan=userData["profileInfo"]["clanName"],
            metadata=userData["profileInfo"]["metaData"],
            unkint=1, # i have no idea what i should put here
            profileIDs=[pid]
        )]
        
        profileInfosList = [profileInfo(**userData["profileInfo"])]
        
        leaderboardStatsList = [([userData["profileInfo"]["personalStatGroupID"],1,33,1,3,0,1,-1,-1,-1,-1,-1,1000,"{}","{}",1740504208]) for i in range (1, 4)]
    
    result = response(
        result=0,
        unknownList=unknownList,
        profileInfos=profileInfosList,
        leaderboardStats=leaderboardStatsList
    )
    
    logger.debug(json.dumps(result, separators=(',', ':'), default=astuple))
    
    return json.dumps(result, separators=(',', ':'), default=astuple)