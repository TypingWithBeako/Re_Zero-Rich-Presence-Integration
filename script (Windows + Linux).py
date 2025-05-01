import time
import pypresence
import argparse
import logging
import re
import platform
import subprocess
from song_metadata import SONGS

# Platform-specific imports
if platform.system() == "Windows":
    import win32gui
else:
    # Check if wmctrl is installed on Linux
    try:
        subprocess.run(["which", "wmctrl"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        logging.error(
            "wmctrl is required but not installed. Please install it with 'sudo apt install wmctrl' or equivalent.")
        exit(1)

parser = argparse.ArgumentParser(description='Discord Rich Presence for Re:Zero Player')
parser.add_argument('interval', nargs='?', type=float, default=1.0,
                    help='Update interval in seconds (default: 1.0)')
args = parser.parse_args()

# Get the interval from command line
update_interval = args.interval

# Log the interval we're using
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logging.info(f"Using update interval: {update_interval} seconds")


def find_chrome_window_with_title(title_fragment=""):
    """Find window that contains Japanese brackets based on platform"""
    if platform.system() == "Windows":
        return find_windows_chrome_window_with_title(title_fragment)
    else:
        return find_linux_chrome_window_with_title(title_fragment)


def find_windows_chrome_window_with_title(title_fragment=""):
    """Find Chrome window that contains Japanese brackets (Windows version)"""
    result = []

    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            # Check for Japanese brackets first (as the primary identifier)
            if "「" in window_title and "」" in window_title:
                # Optionally filter by additional title fragment if provided
                if not title_fragment or title_fragment.lower() in window_title.lower():
                    result.append((hwnd, window_title))

    win32gui.EnumWindows(callback, None)
    return result


def find_linux_chrome_window_with_title(title_fragment=""):
    """Find window that contains Japanese brackets (Linux version)"""
    result = []

    try:
        # Run wmctrl to list all windows with their titles
        output = subprocess.check_output(["wmctrl", "-l", "-p"], text=True)

        # Process each line (window)
        for line in output.splitlines():
            parts = line.split(None, 3)  # Split by whitespace with max 3 splits
            if len(parts) >= 4:
                window_id = parts[0]
                window_title = parts[3]

                # Check for Japanese brackets
                if "「" in window_title and "」" in window_title:
                    # Optionally filter by additional title fragment if provided
                    if not title_fragment or title_fragment.lower() in window_title.lower():
                        result.append((window_id, window_title))
    except subprocess.SubprocessError as e:
        logging.error(f"Error getting window list: {e}")

    return result


def extract_song_info(window_title):
    """Parse window title to get song name"""
    # Assuming format like "「Song Name」 - Re:Zero Player"
    pattern = r"「(.*)」"
    result = re.search(pattern, window_title)
    if result is None:
        return "Does not exist"
    return result.group(1)


# Rich Presence setup
client_id = "1364416390618157176"
RPC = pypresence.Presence(client_id)
RPC.connect()

start_time = time.time()  # Move this line HERE

# Main loop
while True:
    # Initialization
    song_name = None
    artist_name = ""
    image_key = ""

    windows = find_chrome_window_with_title()

    if windows:
        _, window_title = windows[0]
        song_name = extract_song_info(window_title)

        if song_name and song_name in SONGS:
            song_data = SONGS[song_name]
            artist_name = song_data.get("artist", "Unknown Artist")
            image_key = song_data.get("image", "beako_drinking_coffee")

            # Update Discord Rich Presence - Spotify Style
            RPC.update(
                details=f"Đang phát:「{song_name}」",  # Song Title in details
                state=f"◆ {artist_name}",  # Artist in state
                large_image=image_key,  # Song-specific or default image
                large_text=f"{song_name}",  # Tooltip for large image
                start=start_time  # Shows elapsed time
            )
        else:
            RPC.update(
                details="Not in playlist, I suppose.",
                state="Drinking coffee",
                large_image="beako_drinking_coffee",
                large_text="Just drinking coffee, kashira.",
                start=start_time
            )
    else:
        # Default when window not found (Idle state)
        RPC.update(
            details="Idle",
            state="Drinking coffee",
            large_image="beako_drinking_coffee",
            large_text="Just drinking coffee, kashira.",
            start=start_time  # Keeps counting even when idle
        )

    time.sleep(update_interval)  # Use the configured interval (default is 1)