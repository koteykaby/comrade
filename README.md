# COMRADE - A Company of Heroes 2 services reimplementation

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/koteykaby/comrade)

This project is a community-driven emulator for original game services.
Main goal is to make it better playable in LAN parties or in any place where proper internet connection is an issue.

> [!IMPORTANT]
> This is a **single-dev hobby project** developed in limited free time. Stability not guaranteed!
> Currently supports only **Steam (Windows)** version only.

## Discussion

- [Discord Community](https://discord.gg/W4uRYPkZr2)

## Features

## Installation Guide

Here is simple start guide to make it work locally

### Host Setup

1. **Clone repository** and unpack it somewhere
2. **Generate SSL certificate** via `tools/create_ssl.py` and put it to the `ssl` folder
3. **Run the server** via `python -m api.api` and `python -m battleserver.server` (you can also use `scripts/runner.bat`)

### Client Setup

1. **Edit your hosts file**:
    - Windows: `C:\Windows\System32\drivers\etc\hosts`
    - Add new line with your host ip, for example: `192.168.1.100 coh2-api.reliclink.com`
2. **Install SSL certificate** from server's `ssl/` folder
3. **Flush DNS cache** to prevent connecting issues:
    - Run `ipconfig /flushdns` in your terminal
4. **Launch game and try to play!**

## Progress

I think almost all is done for actual playing, but currently it is missing correct battleserver implementation (packet sending/modifying not fully understood). If you have idea - feel free to countribute!

For now is implemented:

- Enter main menu, save progress
- All singleplayer modes (Campaign, Theather of War, Skirmishes)
- Inventory system (with some misunderstanding, but yeah)
- Discover other player lobbies and connect (no actual playing yet)

## Special thanks

Special thanks to @luskaner for his work on <https://github.com/luskaner/ageLANServer> which emulates similar API structure
