import sqlite3
import json
import os
import time
import random
from common.logger import logger

DB_PATH = 'db/server.db'
DEFINITIONS_DB_PATH = 'db/game/item_definitions.sqlite3'

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row 
        return conn

    def _init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            platform_user_id TEXT PRIMARY KEY,
            profile_id INTEGER UNIQUE,
            json_data TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY,
            profile_id INTEGER,
            json_data TEXT,
            FOREIGN KEY(profile_id) REFERENCES users(profile_id)
        )
        ''')
        conn.commit()
        conn.close()

    def _generate_profile_id(self):
        while True:
            new_id = random.randint(1000000, 9999999)
            if not self.get_account_by_profile_id(new_id):
                return new_id

    def _get_all_item_definitions(self):
        if not os.path.exists(DEFINITIONS_DB_PATH):
            logger.error(f"Definitions DB not found: {DEFINITIONS_DB_PATH}")
            return []

        try:
            conn_def = sqlite3.connect(DEFINITIONS_DB_PATH)
            cursor_def = conn_def.cursor()
            
            cursor_def.execute("SELECT id FROM definitions")
                
            rows = cursor_def.fetchall()
            conn_def.close()
            return [row[0] for row in rows]
        except Exception as e:
            logger.error(f"Error reading item definitions: {e}")
            return []

    def _grant_all_items(self, cursor, profile_id):
        logger.info(f"Starting UNLOCK ALL for profile {profile_id}...")
        
        def_ids = self._get_all_item_definitions()
        if not def_ids:
            return

        cursor.execute("SELECT MAX(item_id) FROM inventory")
        row = cursor.fetchone()
        last_id = row[0] if row[0] is not None else 10000
        
        current_time = int(time.time())
        items_to_insert = []
        
        for i, def_id in enumerate(def_ids):
            instance_id = last_id + 1 + i
            
            item_json = {
                "id": instance_id,
                "entityVersion": 0,
                "itemDefinition.id": def_id,
                "profileID": profile_id,
                "durability": 1,
                "durabilityType": 0,
                "metaData": "{\"dlc\":1}",
                "creationDate": current_time,
                "locationID": 0,
                "tradeID": -1,
                "permission": 0,
                "maxChargesPerItem": -1
            }
            items_to_insert.append((instance_id, profile_id, json.dumps(item_json)))

        if items_to_insert:
            cursor.executemany(
                "INSERT INTO inventory (item_id, profile_id, json_data) VALUES (?, ?, ?)",
                items_to_insert
            )
            logger.info(f"Granted {len(items_to_insert)} items to {profile_id}.")

    def create_account(self, platform_user_id: str, alias: str):
        profile_id = self._generate_profile_id()
        final_alias = alias if alias else f"Player_{profile_id}"

        new_account_data = {
            "rlinkAccountInfo": {
                "id": random.randint(1000, 9000),
                "accountName": f"/steam/{platform_user_id}",
                "accountType": 3,
                "ssoID": -1,
                "ssoStatus": 0,
                "country": "us",
                "currency": "usd",
                "spamAllowed": 2,
                "metaData": None
            },
            "profileInfo": {
                "entityVersion": 1,
                "id": profile_id,
                "name": f"/steam/{platform_user_id}",
                "metaData": "",
                "alias": final_alias,
                "clanName": "",
                "personalStatGroupID": random.randint(1000000, 9999999),
                "xp": 0,
                "level": 1,
                "banInfo": None,
                "platformUserID": platform_user_id,
                "leaderboardRegionID": 0,
                "accountType": 3,
                "linkedPlatformAccounts": []
            },
            "characterData": f"[{profile_id},0,0,10,10,0,3500,0,1751500800]",
            "categoryIDs": [],
            "enableCrossplay": 1,
            "privacySettings": [],
            "inventoryFile": ""
        }

        conn = self._get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (platform_user_id, profile_id, json_data) VALUES (?, ?, ?)",
                (platform_user_id, profile_id, json.dumps(new_account_data))
            )

            self._grant_all_items(cursor, profile_id)
            
            conn.commit()
            logger.info(f"Created new account for {platform_user_id}")
            return new_account_data
            
        except Exception as e:
            logger.error(f"Failed to create account: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def get_account_by_steam_id(self, platform_user_id: str):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT json_data FROM users WHERE platform_user_id = ?", (platform_user_id,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row['json_data']) if row else None

    def get_account_by_profile_id(self, profile_id: int):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT json_data FROM users WHERE profile_id = ?", (profile_id,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row['json_data']) if row else None
        
    def get_inventory_items(self, profile_id: int) -> list[dict]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT json_data FROM inventory WHERE profile_id = ?", (profile_id,))
        rows = cursor.fetchall()
        conn.close()
        items = []
        for row in rows:
            if row['json_data']:
                items.append(json.loads(row['json_data']))
        return items

    def save_account(self, account_data: dict):
        steam_id = account_data['profileInfo']['platformUserID']
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET json_data = ? WHERE platform_user_id = ?",
            (json.dumps(account_data), steam_id)
        )
        conn.commit()
        conn.close()
        logger.debug(f"Account {steam_id} saved to DB.")
        
    def update_inventory_item(self, profile_id: int, item_data: dict):
        """Обновляет JSON данные конкретного предмета в инвентаре"""
        item_id = item_data.get('id')
        if item_id is None:
            return

        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE inventory SET json_data = ? WHERE item_id = ? AND profile_id = ?",
                (json.dumps(item_data), item_id, profile_id)
            )
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to update item {item_id}: {e}")
        finally:
            conn.close()

db_manager = DatabaseManager(DB_PATH)

def GetAccount(platformUserID: str):
    return db_manager.get_account_by_steam_id(platformUserID)

def GetAccountByProfileID(profileID: int):
    logger.debug(f"Getting account for profileID: {profileID}")
    
    account = db_manager.get_account_by_profile_id(profileID)
    
    if account:
        return account

    logger.error(f"ProfileID: {profileID} not found.")
    return dict()