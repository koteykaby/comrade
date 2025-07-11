from dataclasses import dataclass

@dataclass
class rlink_info:
    id: int
    accountName: str
    accountType: str
    ssoID: int
    ssoStatus: int
    country: str
    currency: str
    spamAllowed: int
    metaData: str

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
    
class leaderboardstats:
    statGroupID: int
    leaderboardID: int
    wins: int
    losses: int
    streak: int
    disputes: int
    drops: int
    ranking: int
    rankTotal: int
    regionRanking: int
    regionRankTotal: int
    level: int
    rating: int
    counters: str
    itemUseCount: str
    lastMatchTime: int
    
@dataclass
class stat_pl:
    statID: int
    profileID: int
    value: int
    metadata: int
    lastUpdated: int
    
@dataclass
class playerinfo:
    unk: None
    categoryIDs: list[any]
    characterData: str
    enableCrossplay: int
    privacySettings: list[any]
    
@dataclass
class BattleServer:
    name: str
    unk: None
    ip: str
    port1: int
    port2: int
    port3: int
    
@dataclass
class PresenceProfile:
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
    presenceID: int
    presenceLocalized: None
    presencePropertyInfo: list
    
@dataclass
class PlatformSessionUpdateMessage:
    status_code: int
    description: str
    host_id: int
    lobby_ids: any

# information for peer information in the MatchStartMessage packet
@dataclass
class peer_values:
    profileID: int 
    unk_data: any
    # 231430
    # 231451
    # 317850
@dataclass
class peer_definitions:
    profile_id: str
    peer_id: str
@dataclass
class peer_inventory:
    profile_id: str
    items: any
    
@dataclass
class MatchStartMessage:
    status_code: int
    description: str
    profile_id: int
    other_data: any