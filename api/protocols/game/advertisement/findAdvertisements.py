from api.protocols.game.advertisement.structures import AdvertisementsList

def advertisement_findAdvertisements(lobby_list):
    result = AdvertisementsList(
        status_code=0,
        advertisements=lobby_list,
        unknown_null=[]
    )
    return result
