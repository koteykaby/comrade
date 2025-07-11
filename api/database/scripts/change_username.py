from api.database.main import create_session
from api.database.interract import get_userdata

def change_username(id, username):
    db_session = create_session()
    account = get_userdata(account_id=id)
    
    data = account.data
    data['profile_info']['alias'] = str(username)
    
    print(f"[Database] Enum changed in server db: {username}")
    
    db_session.commit()
    db_session.close()