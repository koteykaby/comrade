from api.protocols.game.item.getInventoryByProfileIDs import getInventoryByProfileIDs

from api.database import interract
from api.utils import datautils

from dataclasses import dataclass

@dataclass
class InventoryItem:
    id: int
    entityVersion: int
    itemDefinition_id: int
    profileID: int
    durability: int
    durabilityType: int
    metaData: str
    creationDate: int
    locationID: int
    tradeID: int
    permission: int
    maxChargesPerItem: int
    
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
class move_items:
    unk: int
    maybe_pos: any
    items_list: any

def fetch_inventory_data(profileID):
    account_data = interract.get_userdata(account_id=profileID)
    
    print(account_data)
    
    inventory_items = [list(item.values()) for item in account_data.inventory]
    Item_locations = [list(item.values()) for item in account_data.item_locations]
    
    result = getInventoryByProfileIDs(profile_id=profileID,
                                      inventory_items=inventory_items,
                                      item_locations=Item_locations)
    return datautils.relicjson(result)
