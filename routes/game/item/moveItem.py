import json
from common.logger import logger
from managers import sessions

from managers.account import db_manager 

async def Handle(sessionID, itemIDs, itemLocationIDs):
    logger.info(
        f"Moving items {itemIDs} to locations {itemLocationIDs}, sessionID: {sessionID}"
    )

    try:
        item_ids = json.loads(itemIDs)
        item_location_ids = json.loads(itemLocationIDs)
    except Exception as e:
        logger.error(f"JSON Parse error: {e}")
        return json.dumps([1, [], []])

    if len(item_ids) != len(item_location_ids):
        logger.error("itemIDs and itemLocationIDs length mismatch")
        return json.dumps([1, [], []])

    sessionData = sessions.GetSession(sessionID)
    if not sessionData:
        logger.error(f"Session {sessionID} not found")
        return json.dumps([1, [], []])
        
    pID = sessionData["profileInfo"]["id"]

    inventoryItems = db_manager.get_inventory_items(pID)
    if not inventoryItems:
        logger.warning(f"Inventory is empty or not found for {pID}")
        inventoryItems = []

    final_locations = {}
    for item_id, location_id in zip(item_ids, item_location_ids):
        final_locations[item_id] = location_id

    response_items_buffer = []
    
    for item in inventoryItems:
        item_id = item.get("id")

        if item_id in final_locations:
            new_location = final_locations[item_id]
            current_location = item.get("locationID")

            if current_location != new_location:
                item["locationID"] = new_location
                item["entityVersion"] = item.get("entityVersion", 0) + 1
                
                logger.info(f"Item {item_id}: loc {current_location} -> {new_location}, ver -> {item['entityVersion']}")
                
                db_manager.update_inventory_item(pID, item)
            
            response_items_buffer.append(item)

    global_result = 0
    op_results = [0] * len(item_ids)
    serialized_items = []

    for item in response_items_buffer:
        item_array = [
            item.get("id"),
            item.get("entityVersion"),
            item.get("itemDefinition.id"),
            item.get("profileID"),
            item.get("durability", 1),
            item.get("durabilityType", 0),
            item.get("metaData", ""),
            item.get("creationDate"),
            item.get("locationID"),
            item.get("tradeID", -1),
            item.get("permission", 0),
            item.get("maxChargesPerItem", -1)
        ]
        serialized_items.append(item_array)
        
    logger.debug(f"Serialized response: {serialized_items}")
    
    sessionData["equipedItems"] = serialized_items

    return json.dumps([global_result, op_results, serialized_items])