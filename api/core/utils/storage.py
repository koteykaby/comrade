import json

lastsession = 1
users = {}

def create_session(steamID,
                   username,
                   profileID,
                   sessionid=str(lastsession)):
    user = {
        str(sessionid): {
            "steamID": steamID,
            "profileID": profileID,
            "username": username
        }
    }
    print(f'[storage] {steamID}|{username} got session id {sessionid}')
    global users
    users.update(user)
    print(f"!!debug!!: {users}")
    global lastsession
    lastsession+=1
    return json.dumps(users)