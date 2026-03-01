from dataclasses import dataclass, astuple
import json

from singletons import achievements
from common.logger import logger

@dataclass
class response:
    result: int
    achievedAchievements: list

@dataclass
class achievement:
    achievement_id: int
    achievedDate: int

@dataclass
class achievementsList:
    profileID: int
    grantedAchievements: list[achievement]

async def Handle(profileIDs):
    pids = json.loads(profileIDs)
    
    logger.debug(f"Requesting achievements for profiles: {pids}")
    
    valid_achievements = []

    def parse_raw_list(raw_list):
        parsed = []
        for item in raw_list:
            a_id = item.get("achievement.id") or item.get("achievementId") or item.get("achievement_id")
            
            if a_id is not None:
                parsed.append(
                    achievement(
                        achievement_id=int(a_id),
                        achievedDate=int(item.get("achievedDate", 0))
                    )
                )
        return parsed

    if hasattr(achievements, "values"):
        for val in achievements.values():
            if isinstance(val, dict):
                info = val.get("m_achievementsEvent.m_info", {})
                raw_list = info.get("grantedAchievements")
                
                if raw_list:
                    valid_achievements.extend(parse_raw_list(raw_list))
                
                elif "grantedAchievements" in val:
                    valid_achievements.extend(parse_raw_list(val["grantedAchievements"]))

    elif isinstance(achievements, dict):
        info = achievements.get("m_achievementsEvent.m_info", {})
        raw_list = info.get("grantedAchievements")
        if raw_list:
             valid_achievements.extend(parse_raw_list(raw_list))

    result = response(
        result=0,
        achievedAchievements=[
            achievementsList(
                profileID=pid,
                grantedAchievements=valid_achievements
            )
            for pid in pids
        ]
    )
    
    return json.dumps(result, separators=(",", ":"), default=astuple)