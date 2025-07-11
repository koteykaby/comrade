from dataclasses import dataclass

@dataclass
class IDs_fields:
    statGroupID: int
    unk_str: str
    unk_str1: str
    unk_int: int
    profileID: any # [profileID]

@dataclass
class profile:
    entityVersion: int
    id: int
    name: str
    metaData: str
    alias: str
    clanName: str
    personalStatGroupID: str
    xp: int
    level: int
    leaderboardRegionID: int
    banInfo: int
    platformUserID: str
    accountType: int # 3 - steam
    linkedPlatformAccounts: list[any]

@dataclass
class StatGroupsList_resp:
    status_code: int
    ids: IDs_fields
    profile_info: profile
    leaderboards: any
