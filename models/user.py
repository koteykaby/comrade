from dataclasses import dataclass

@dataclass
class accountInfo:
    id: int
    accountName: str
    accountType: int
    ssoID: int
    ssoStatus: int
    country: str
    currency: str
    spamAllowed: int
    metaData: None

@dataclass
class profileInfo:
    entityVersion: int
    id: int
    name: str
    metaData: str
    alias: str
    clanName: str
    personalStatGroupID: int
    xp: int
    level: int
    leaderboardRegionID: int
    banInfo: None
    platformUserID: str
    accountType: int
    linkedPlatformAccounts: list
    
@dataclass
class additionalProfileInfo:
    result: int
    profile: profileInfo
    social: list
    leaderboardStats: list
    otherStats: list
    unknownNull: None
    categoryIDs: list
    characterData: str
    enableCrossplay: int
    privacySettings: list
    
@dataclass
class profilePresenceInfo:
    entityVersion: int
    id: int
    name: str
    metaData: str
    alias: str
    clanName: str
    personalStatGroupID: int
    xp: int
    level: int
    leaderboardRegionID: int
    banInfo: None
    platformUserID: str
    accountType: int
    linkedPlatformAccounts: list[str]
    presenceID: int
    presenceLocalized: None
    presenceProperty: list[str]