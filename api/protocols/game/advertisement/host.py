from api.protocols.game.advertisement.structures import Peer, battleserver_authtoken

def advertisement_host(advertisementid,
                       address,
                       ports,
                       relayRegion,
                       profileID,
                       party,
                       statGroupID,
                       raceID,
                       team):
    result = battleserver_authtoken(
        status_code=0,
        advertisementid=advertisementid,
        description="authtoken",
        address=address,
        port1=ports[0],
        port2=ports[1],
        port3=ports[2],
        relayRegion=relayRegion,
        peerList=[
            Peer(
                advertisementID=advertisementid,
                profileID=profileID,
                party=party,
                statGroupID=statGroupID,
                raceID=raceID,
                team=team,
                route="/10.0.7.136"
            )
        ],
        unk=0,
        unk1="0"
    )
    return result