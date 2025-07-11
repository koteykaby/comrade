# generated with ai

import requests
import json
from typing import Optional, Dict, Any, List, Union

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings()

class Coh2LobbyManager:
    def __init__(self, platform_user_id: str, alias: str = "player"):
        """
        Initialize the lobby manager with user credentials.
        
        Args:
            platform_user_id: Steam ID or other platform identifier
            alias: Player display name
        """
        self.base_url = "https://coh2-api.reliclink.com/game"
        self.session = requests.Session()
        self.platform_user_id = platform_user_id
        self.alias = alias
        self.session_id = None
        self.match_id = None
        self.auth_token = None
        self.server_info = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with the server and retrieve session ID.
        
        Returns:
            bool: True if authentication succeeded
        """
        url = f"{self.base_url}/login/platformlogin"
        params = {
            "platformUserID": self.platform_user_id,
            "alias": self.alias
        }
        
        try:
            response = self.session.post(url, params=params, verify=False)
            response.raise_for_status()
            
            # Parse response to get session ID (second value in JSON array)
            auth_data = response.json()
            if isinstance(auth_data, list) and len(auth_data) >= 2:
                self.session_id = auth_data[1]
                print(f"Authentication successful. SessionID: {self.session_id}")
                return True
            else:
                print("Invalid authentication response format")
                return False
                
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False
    
    def read_session(self, ack: bool = False) -> Optional[Dict[str, Any]]:
        """
        Read session information from the server.
        
        Args:
            ack: Whether to acknowledge the session read
            
        Returns:
            dict: Session information if successful, None otherwise
        """
        if not self.session_id:
            print("SessionID not set. Authenticate first.")
            return None
            
        url = f"{self.base_url}/login/readSession"
        params = {
            "sessionID": self.session_id,
            "ack": int(ack)  # Convert bool to 0/1
        }
        
        try:
            response = self.session.post(url, params=params, verify=False)
            response.raise_for_status()
            session_info = response.json()
            print("Session information:")
            print(json.dumps(session_info, indent=2))
            return session_info
        except Exception as e:
            print(f"Failed to read session: {str(e)}")
            return None
    
    def parse_host_response(self, response_data: List[Union[int, str]]) -> bool:
        """
        Parse the host response to extract match ID and other information.
        
        Args:
            response_data: The list response from host endpoint
            
        Returns:
            bool: True if parsing was successful
        """
        try:
            # Response format: [0, matchID, "authtoken", ...]
            if len(response_data) >= 3 and isinstance(response_data[1], int):
                self.match_id = response_data[1]
                self.auth_token = response_data[2]
                
                # Extract server information if available
                if len(response_data) >= 8:
                    self.server_info = {
                        'ip': response_data[3],
                        'ports': response_data[4:7],
                        'region': response_data[7]
                    }
                
                print(f"Match created successfully. MatchID: {self.match_id}")
                print(f"Auth token: {self.auth_token}")
                if self.server_info:
                    print(f"Server info: {self.server_info}")
                return True
            return False
        except Exception as e:
            print(f"Failed to parse host response: {str(e)}")
            return False
    
    def create_lobby(self) -> bool:
        """
        Create a new game lobby.
        
        Returns:
            bool: True if lobby creation succeeded
        """
        if not self.session_id:
            print("SessionID not set. Authenticate first.")
            return False
            
        url = f"{self.base_url}/advertisement/host"
        params = {
            "advertisementid": -1,
            "appbinarychecksum": 24336,
            "automatchPoll_id": -1,
            "callNum": 20,
            "connect_id": 1,
            "datachecksum": 237719574,
            "description": "SESSION_MATCH_KEY",
            "hostid": "1",
            "isObservable": 1,
            "lastCallTime": 5346,
            "mapname": "2p_coh2_resistance",
            "matchtype": 21,
            "maxplayers": 8,
            "moddllchecksum": 0,
            "moddllfile": "INVALID",
            "modname": "INVALID",
            "modversion": "INVALID",
            "observerDelay": 180,
            "observerPassword": 0,
            "options": "eNozYPvGgADsQJycn1uUmJLKyMDECBP+DwUgthyjHIjEg0FACIiNCuKT8zOM4otSizOLSxLzklMZBgMAAItmFCk=",
            "party": -1,
            "password": 0,
            "passworded": 0,
            "race": 1,
            "relayRegion": "comrade",
            "serviceType": 0,
            "sessionID": self.session_id,
            "slotinfo": "eNrtkDELwjAQhf0tN0cxjp2LULAg1U0cjvSCwSYpySkU8b9LIqirYyHb97gH9/jkRpweMAavzUCN035leqiWUkBkZONdU78jE9rEawEa1e8loKIvu+uO7jTkYkotsrocp/FTYWNpT2Eb0FJ7yD0TO8J+ypze3mJGS4w1MkIF8BR/rZSzWFlcFpfF5dxcnhcvxNmdZw==",
            "state": 1,
            "statgroup": -1,
            "team": -1,
            "versionFlags": 0,
            "visible": 1
        }
        
        try:
            response = self.session.post(url, params=params, verify=False)
            response.raise_for_status()
            
            # Parse the response to get match ID and other info
            response_data = response.json()
            if self.parse_host_response(response_data):
                return True
            else:
                print("Failed to extract match ID from response")
                return False
                
        except Exception as e:
            print(f"Failed to create lobby: {str(e)}")
            return False
    
    def update_platform_lobby_id(self, platform_lobby_id: str) -> bool:
        """
        Update the platform-specific lobby ID (e.g., Steam Lobby ID).
        
        Args:
            platform_lobby_id: The platform-specific lobby identifier
            
        Returns:
            bool: True if update succeeded
        """
        if not self.session_id or not self.match_id:
            print("SessionID or MatchID not set.")
            return False
            
        url = f"{self.base_url}/advertisement/updatePlatformLobbyID"
        params = {
            "callNum": 51,
            "connect_id": 1,
            "lastCallTime": 9513,
            "matchID": self.match_id,
            "platformlobbyID": platform_lobby_id,
            "sessionID": self.session_id
        }
        
        try:
            response = self.session.post(url, params=params, verify=False)
            response.raise_for_status()
            print(f"Platform lobby ID updated to {platform_lobby_id}")
            print("Server response:", response.text)
            return True
        except Exception as e:
            print(f"Failed to update platform lobby ID: {str(e)}")
            return False
    
    def add_player_to_lobby(self, profile_id: int, race_id: int, 
                          statgroup_id: int, team_id: int = 0) -> bool:
        """
        Add a player to the existing lobby.
        
        Args:
            profile_id: Player's profile ID
            race_id: Player's race/faction ID
            statgroup_id: Player's stat group ID
            team_id: Team number (default 0)
            
        Returns:
            bool: True if player was added successfully
        """
        if not self.session_id or not self.match_id:
            print("SessionID or MatchID not set.")
            return False
            
        url = f"{self.base_url}/party/peerAdd"
        params = {
            "callNum": 21,
            "connect_id": 2,
            "lastCallTime": 5849,
            "match_id": self.match_id,
            "profile_ids": f"[{profile_id}]",
            "race_ids": f"[{race_id}]",
            "sessionID": self.session_id,
            "statGroup_ids": f"[{statgroup_id}]",
            "teamIDs": f"[{team_id}]",
        }
        
        try:
            response = self.session.post(url, params=params, verify=False)
            response.raise_for_status()
            print(f"Player {profile_id} added to lobby successfully")
            print("Server response:", response.text)
            return True
        except Exception as e:
            print(f"Failed to add player: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    # Replace with your actual platformUserID
    lobby_manager = Coh2LobbyManager(
        platform_user_id="76561198617872072", 
        alias="player"
    )
    
    # 1. Authenticate
    if lobby_manager.authenticate():
        # 2. Read session information (with ack=True if needed)
        lobby_manager.read_session(ack=True)
        
        # 3. Create lobby
        if lobby_manager.create_lobby():
            # 4. Update platform lobby ID (e.g., Steam Lobby ID)
            lobby_manager.update_platform_lobby_id("109775242837458806")
            
            # 5. Add players to lobby (example)
            lobby_manager.add_player_to_lobby(
                profile_id=3, 
                race_id=3, 
                statgroup_id=2, 
                team_id=0
            )
            pass