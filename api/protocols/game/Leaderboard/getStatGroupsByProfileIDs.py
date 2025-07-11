from api.protocols.game.Leaderboard.structures import StatGroupsList_resp, IDs_fields, profile

def Leaderboard_getStatGroupsByProfileIDs(id, profile_info, name, u_leaderboardStats, banState):
    data = StatGroupsList_resp(
        status_code=0,
        ids=IDs_fields(
            statGroupID=id,
            unk_str="",
            unk_str1="",
            unk_int=1,
            profileID=[id]
        ),
        profile_info=profile(
            **profile_info,
            id=id, personalStatGroupID=id, banInfo=banState
        ),
        leaderboards=(
            [list(obj.values()) for obj in u_leaderboardStats]
        )
    )
    
    return data