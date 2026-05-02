import json
import os
from datetime import datetime

# Files used for local data storage, acting as a lightweight replacement for a real database.
PLAYERS_FILE = "players.json"
SESSIONS_FILE = "sessions.json"


def _load_json(filepath):
    """
    Loads and parses data from a JSON file. 
    Returns an empty list if the file does not exist or is corrupted, 
    preventing FileNotFoundError or JSONDecodeError from crashing the game.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return []


def _save_json(filepath, data):
    """Saves a Python dictionary or list to a JSON file with pretty formatting."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def setup_database():
    """
    Previously used to execute PostgreSQL 'CREATE TABLE' queries.
    Now, it simply initializes empty JSON files if they don't already exist on the disk,
    ensuring the game has a place to read/write data upon first launch.
    """
    if not os.path.exists(PLAYERS_FILE):
        _save_json(PLAYERS_FILE, [])
    if not os.path.exists(SESSIONS_FILE):
        _save_json(SESSIONS_FILE, [])
    print("Storage ready (JSON mode).")


def get_or_create_player(username):
    """
    Searches for an existing player by their username (case-insensitive).
    If found, returns their unique ID. If not found, generates a new sequential ID,
    creates a new player record, saves it, and returns the new ID.
    """
    players = _load_json(PLAYERS_FILE)

    # Look for an existing player
    for player in players:
        if player["username"].lower() == username.lower():
            return player["id"]

    # Player not found — generate a new ID based on the highest existing ID
    new_id = (max(p["id"] for p in players) + 1) if players else 1
    players.append({"id": new_id, "username": username})
    _save_json(PLAYERS_FILE, players)
    return new_id


def save_score(player_id, score, level):
    """Appends the results of the current game session to the sessions JSON file."""
    sessions = _load_json(SESSIONS_FILE)

    sessions.append({
        "player_id": player_id,
        "score": score,
        "level_reached": level,
        "played_at": datetime.now().strftime("%Y-%m-%d")
    })

    _save_json(SESSIONS_FILE, sessions)


def get_top_10():
    """
    Retrieves the top 10 best scores across all players.
    Returns a list of tuples formatted as (username, score, level_reached, played_at).
    This matches the exact output format previously returned by PostgreSQL, 
    meaning 'main.py' doesn't need to be modified.
    """
    players = _load_json(PLAYERS_FILE)
    sessions = _load_json(SESSIONS_FILE)

    # Create a dictionary mapping player IDs to their usernames for O(1) lookups
    id_to_name = {p["id"]: p["username"] for p in players}

    # Construct the final row format by matching session player_ids to usernames
    rows = []
    for s in sessions:
        username = id_to_name.get(s["player_id"], "Unknown")
        rows.append((username, s["score"], s["level_reached"], s["played_at"]))

    # Sort the list by the second element in the tuple (score) in descending order
    rows.sort(key=lambda x: x[1], reverse=True)
    return rows[:10]


def get_personal_best(player_id):
    """Returns the highest score for a specific player, or 0 if they have no recorded sessions."""
    sessions = _load_json(SESSIONS_FILE)

    scores = [s["score"] for s in sessions if s["player_id"] == player_id]
    return max(scores) if scores else 0