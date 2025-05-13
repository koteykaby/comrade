# Server emulator for Company of Heroes 2

Mainly focuses on making the game work on LAN without any services relation

> [!] IMPORTANT
> Currently supports only Steam version. Pirated copies is not supported and not will be.

## Usage

Here is a small guide for deploying and connecting to the server

### Host

1. Generate SSL cetificate and key with `genssl.py` tool, share it with clients
2. Put it to the `ssl` folder in the comrade main folder
3. Edit `config/config.json` (specify your host IP-address)
4. Run api with `api/api.py` (`python -m api.api`)

### Client

1. Install SSL certificate from the host to your system
2. Add `coh2-api.reliclink.com` to the your hosts file
3. Try to start the game

## Account creation

There is no any account creation tool for now, so you need to do it manually.
To do it, open the `db/example.json` with your text editor and change all id's, steamid's and statGroupIDs for your needs.
Save it with your steamid in the name, for example `76561198617872072.json`

## Progress

Now you can get into the game menu and play SP missions (Theater of War, Campaign), but skirmishes still doesn't work.
