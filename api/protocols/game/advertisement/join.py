from api.protocols.game.advertisement.structures import join_advertisement_resp, Peer

def advertisements_join(address, ports, advid, p_id, party, r_id, t_id):
    data = join_advertisement_resp(
        status_code=0,
        route="/10.0.7.136",
        address=address,
        port1=ports[0],
        port2=ports[1],
        port3=ports[2],
        peers=[Peer(
            advertisementID=int(advid),
            profileID=int(p_id),
            party=int(party),
            statGroupID=int(p_id),
            raceID=int(r_id),
            team=int(t_id),
            route="/10.0.7.136"
        )]
    )
    return data