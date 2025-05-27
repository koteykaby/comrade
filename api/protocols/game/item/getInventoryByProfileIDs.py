from dataclasses import dataclass

@dataclass
class Inventory:
    unk: int
    inventoryItems: any
    itemLocations: any
    
def getInventoryByProfileIDs(profile_id, inventory_items, item_locations):
    data = Inventory(
        unk=0,
        inventoryItems=[[profile_id, inventory_items]],  
        itemLocations=[[profile_id, item_locations]] 
    )
    return data