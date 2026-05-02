import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid_overlay": True,
    "sound": True
}

def load_settings():
    # Check if the settings file exists; if not, create it with default values 
    # to ensure the game has a baseline configuration to run.
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(SETTINGS_FILE, "r") as f:
            user_settings = json.load(f)

        # Iterate through default settings to add any missing keys to the user's file.
        # This acts as backward compatibility (protection against outdated configs) 
        # in case new settings were added in an update.
        updated = False
        for key, value in DEFAULT_SETTINGS.items():
            if key not in user_settings:
                user_settings[key] = value
                updated = True

        if updated:
            save_settings(user_settings)

        return user_settings
    except (json.JSONDecodeError, Exception):
        # If the JSON file is corrupted or unreadable, overwrite it with defaults 
        # to prevent the application from crashing during startup.
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_settings(settings):
    # Opens the file in write mode ("w") and dumps the dictionary as formatted JSON
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)