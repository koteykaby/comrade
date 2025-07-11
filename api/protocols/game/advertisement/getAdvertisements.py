from api.protocols.game.advertisement.structures import get_advertisements_resp

def advertisement_getAdvertisements(advs):
    data = get_advertisements_resp(
        status_code=0,
        advertisements=advs
    )
    return data