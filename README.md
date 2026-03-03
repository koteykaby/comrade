# COMRADE - Dedicated Server for Company of Heroes 2

You can find more in our [Discord](https://discord.gg/KTx7uhWsTB)

This project is community-driven dedicated server designed to play the game on LAN and preserve the game for ages. Currenty WIP.

## What works

- Authenticate, fetch settings, etc.
- Singleplayer missions (Theater of War, Campaign)
- Inventory (all items are unlocked)
- Matchmaking and ToW Co-op missions (requires external BattleServer)

## What doesn't works

- Authenticate for other platforms such as Xbox
- Saving stats locally in the game
- Observing (not implemented)
- Leveling
- Leaderboards
- Automatch (use "Public games list" button instead)
- In-game menu chat (looks like it even broke in the game)
- In-game shop (disabled)
- Maybe something other I forgot

## Usage

Here is a quick-start guide to running and playing the game.

### Server

1. Generate an SSL certificate and private key using the `certgen.py` script in the `tools` folder. Share the certificate with your peers.
2. Configure the server by editing `config/services.json` (update the IPs to match your host).
3. Run the server with `python ./main.py`.

### Client

1. Install the SSL certificate from your host. On Windows:
    - Open `certmgr.msc`.
    - Open `Trusted Root Certificate Authorities/Certificates`.
    - Click `Action -> All Tasks -> Import` and import the certificate.
2. Update the hosts file. On Windows:
    - Open `C:/Windows/System32/drivers/etc` and open the `hosts` file with Notepad.
    - Add `127.0.0.1 coh2-api.reliclink.com` to it.
    > [!Note]
    > Replace `127.0.0.1` with your server's host IP.
    - Run `ipconfig /flushdns` in PowerShell.
3. Run the game and play.

## Legal Disclaimer

This is **not** affiliated, associated, authorized, endorsed by, or in any way officially connected with **Relic Entertainment**, **SEGA**, or any of their subsidiaries or affiliates.

The names *Company of Heroes 2* as well as related names, marks, emblems, and images are registered trademarks of their respective owners. This project is for educational and preservation purposes only.
