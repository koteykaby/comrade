# Dedicated Server Emulation stuff for Company of Heroes 2

This project is a community-driven emulator for original game services.
Main goal is to make it better playable in LAN parties or in any place where proper internet connection is a problem.

If you want to discuss about it - join our [Discord community](https://discord.gg/W4uRYPkZr2)!

> [!IMPORTANT]
> Currently have support only for Steam (Windows) version.

## Usage

Download latest server files from sources or [release](https://github.com/koteykaby/comrade/releases/latest)

### Host

1. Install depedencies with `pip install -r requirements.txt`
2. Generate self-signed SSL certificates. You can use `tools/create_ssl.py` for it. Put certificate and private key to the `ssl` folder in the project root
3. Modify config file in the `config` folder for your needs (change IP's)
4. Open port tcp/443 for your clients (allow in the firewall)
5. Run API with `python -m api.api`

### Client

1. Modify your hosts file with binding original to your host IP. For example `127.0.0.1 coh2-api.reliclink.com`. Also run `ipconfig /flushdns` command to prevent connecting issues
2. Install self-signed SSL certificates from host to your system
3. Try to run the game. API will automatically create account for you

## Progress

For now is implemented:

- Entering main menu, fetch some data
- Start any singleplayer game (Campaign, Theater of War) (no skirmishes yet)
