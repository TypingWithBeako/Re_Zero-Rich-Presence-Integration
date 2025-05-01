# Re:Zero Discord Rich Presence Integration

[![Discord](https://img.shields.io/badge/Discord-Rich%20Presence-7289DA.svg)](https://discord.com)

Display your currently playing Re:Zero songs on Discord with custom artwork and information. Automatically detects song titles from your browser window and updates your Discord status in real time.

## Quick Start Guide

1. **Make sure Discord is running first** (very important!)
2. Open your browser with Re:Zero Player (English/Vietnamese version)
3. Run the executable for your system:
   - **Windows:** Double-click `ReZero_Discord_Presence (Windows).exe`
   - **Linux:** Run `./ReZero_Discord_Presence\ \(Arch\ Linux\)`

That's it! Your Discord status will now show your currently playing Re:Zero music.

## Requirements

- **Discord desktop application** (must be running before starting this integration)
- Browser window with Re:Zero Player (showing song titles in Japanese brackets 「」)
- For Linux users: `wmctrl` utility (`sudo pacman -S wmctrl` on Arch-based systems)

## Autostart Setup

### Windows
1. Press `Win+R`, type `shell:startup` and press Enter
2. Create a shortcut to `ReZero_Discord_Presence (Windows).exe` in this folder

### Linux
Create a systemd user service:
```bash
mkdir -p ~/.config/systemd/user/
echo '[Unit]
Description=Re:Zero Rich Presence
After=graphical-session.target discord.service

[Service]
Type=simple
ExecStartPre=/usr/bin/sleep 5
ExecStart=/home/YourUsername/path/to/ReZero_Discord_Presence\ \(Arch\ Linux\)
Restart=on-failure

[Install]
WantedBy=graphical-session.target' > ~/.config/systemd/user/rezero-presence.service

systemctl --user enable rezero-presence.service
```
## Troubleshooting

- **No Discord presence showing:** Make sure Discord is running before starting the executable
- **No song detected:** Ensure your browser window title contains Japanese brackets (「」)
- **Linux executable won't run:** Make it executable with `"chmod +x ReZero_Discord_Presence\ \(Arch\ Linux\)"`

## Advanced Usage

For those who want to run from source or modify the code:
- Source files are provided: `script (Windows).py`, `script (Windows + Linux).py`, and `song_metadata.py`
- Python 3.6+ is required
- Install dependencies: `pip install pypresence` (and `pywin32` for Windows)
- Run with a custom update interval: `python "script (Windows + Linux).py" 5`

## Contributing

Feel free to add more songs to the database in `song_metadata.py` or submit improvements via GitHub!
