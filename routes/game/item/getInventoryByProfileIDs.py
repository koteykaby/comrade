from dataclasses import dataclass, astuple
import json

from managers.account import db_manager as db 
from singletons import itemLocations

@dataclass
class ItemLocation:
    id: int
    entityVersion: int
    locationID: int
    categoryID: int
    maxItems: int
    locked: int
    isPublic: int
    isForMatch: int
    tracksMoves: int
    
@dataclass
class ItemInstance:
    id: int
    entityVersion: int
    itemDefinitionID: int
    profileID: str
    durability: int
    durabilityType: int
    metaData: str
    creationDate: int
    locationID: int
    tradeID: int
    permission: int
    maxChargesPerItem: int

@dataclass
class InventoryItemsData:
    profileID: str
    items: list[ItemInstance]
    
@dataclass
class InventoryLocationsData:
    profileID: str
    locations: list[ItemLocation]

@dataclass
class InventoryItemsResult:
    result: int
    inventoryItemsData: list
    inventoryLocationsData: list

async def Handle(sessionID: str, profileIDs: str):
    profileIDs_list = json.loads(profileIDs)
    target_profile_id = profileIDs_list[0]
    items_from_db = db.get_inventory_items(int(target_profile_id))
    
    result = InventoryItemsResult(
        result=0,
        inventoryItemsData=[
            InventoryItemsData(
                profileID=str(target_profile_id),
                items=[
                    ItemInstance(
                        id=item["id"],
                        entityVersion=item["entityVersion"],
                        itemDefinitionID=item["itemDefinition.id"], 
                        profileID=item["profileID"],
                        durability=item["durability"],
                        durabilityType=item["durabilityType"],
                        metaData=item["metaData"],
                        creationDate=item["creationDate"],
                        locationID=item["locationID"],
                        tradeID=item["tradeID"],
                        permission=item["permission"],
                        maxChargesPerItem=item["maxChargesPerItem"]
                    ) for item in items_from_db 
                ]
            ),
        ],
        inventoryLocationsData=[
            InventoryLocationsData(
                profileID=str(target_profile_id),
                locations=[
                    ItemLocation(
                        id=loc["id"],
                        entityVersion=loc["entityVersion"],
                        locationID=loc["locationID"],
                        categoryID=loc["categoryID"],
                        maxItems=loc["maxItems"],
                        locked=loc["locked"],
                        isPublic=loc["isPublic"],
                        isForMatch=loc["isForMatch"],
                        tracksMoves=loc["tracksMoves"]
                    ) for loc in itemLocations["m_GetInventoryItemsEvent.m_info.itemLocations"]
                ]
            ),
        ]
    )

    return json.dumps(result, separators=(",", ":"), default=astuple)