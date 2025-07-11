from api.protocols.game.item.getInventoryByProfileIDs import getInventoryByProfileIDs
from api.protocols.game.item.moveItems import item_moveItems

from api.database import interract
from api.utils import datautils
from api.core.sessions import sessions_data

from dataclasses import dataclass
import json

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

def fetch_inventory_data(profileID):
    account_data = interract.get_userdata(account_id=profileID)

    inventory_items = [list(item.values()) for item in account_data.inventory]
    Item_locations = [list(item.values()) for item in account_data.item_locations]
    
    result = getInventoryByProfileIDs(profile_id=profileID,
                                      inventory_items=inventory_items,
                                      item_locations=Item_locations)
    return datautils.relicjson(result)

def moveItems(sessionID, itemIDs, itemLocationIDs):
    session = sessions_data[f'{sessionID}']
    account = interract.get_userdata(account_id=session['account'])
    inventory = account.inventory
    
    if isinstance(itemIDs, str):
        itemIDs = json.loads(itemIDs)
    if isinstance(itemLocationIDs, str):
        itemLocationIDs = json.loads(itemLocationIDs)
    
    items_dict = {item['id']: item for item in inventory if item['id'] in itemIDs}
    
    previous_itemLocationsIDs = []
    result_itemLocationsIDs = []
    
    for item_id, new_location in zip(itemIDs, itemLocationIDs):
        if item_id not in items_dict:
            continue  
            
        item = items_dict[item_id]
        previous_itemLocationsIDs.append(item["locationID"])
        item["locationID"] = new_location
        
        result_itemLocationsIDs.append(item.copy())
        
    session['equiped_items'] = [list(item.values()) for item in result_itemLocationsIDs]
    print(f"[Inventory] DEBUG: {json.dumps(session)}")
        
    result = item_moveItems(previous_pos=previous_itemLocationsIDs,
                            target_items=[list(item.values()) for item in result_itemLocationsIDs])
    print(f"[Inventory] moveItems result! {result}")
        
    return result