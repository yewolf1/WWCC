from pathlib import Path
import json
import os
from dotenv import load_dotenv

load_dotenv()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID", "")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET", "")

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "twitch_controller"
CONFIG_PATH = CONFIG_DIR / "twitch_config.json"
TOKENS_PATH = CONFIG_DIR / "twitch_tokens.json"

DEFAULT_CONFIG = {
    "client_id": TWITCH_CLIENT_ID,
    "client_secret": TWITCH_CLIENT_SECRET,
    "scopes": ["CHANNEL_READ_REDEMPTIONS"],
    "rewards": {
        "Kill Link": ["kill"],

        "1/4 heart": ["hp", "--quarter"],
        "3 hearts": ["hp", "--three"],
        "Set HP to 10 hearts": ["hp", "--set", "10"],

        "Unequip slot X": ["unequip", "--slot", "x"],
        "Unequip slot Y": ["unequip", "--slot", "y"],
        "Unequip slot Z": ["unequip", "--slot", "z"],
        "Unequip all slots": ["unequip", "--all"],

        "Sword (viewer choice)": ["__sword_choice__"],
        "Shield (viewer choice)": ["__shield_choice__"],
        "Tunic (viewer choice)": ["__tunic_choice__"],

        "Rupees +50": ["rupees", "--add", "50"],
        "Rupees -50": ["rupees", "--add", "-50"],
        "Rupees set to 0": ["rupees", "--set", "0"],
        "Rupees max wallet": ["rupees", "--set", "5000"],

        "Wallet: Tier 0": ["wallet", "--tier", "0"],
        "Wallet: Tier 1": ["wallet", "--tier", "1"],
        "Wallet: Tier 2": ["wallet", "--tier", "2"],
        "Wallet: Cycle": ["wallet", "--cycle"],

        "Time (viewer choice)": ["__time_choice__"],
        "Weather (viewer choice)": ["__weather_choice__"],

        "Freeze ON": ["freeze", "--on"],
        "Freeze OFF": ["freeze", "--off"],
        "Freeze 10s": ["freeze", "--timer", "10"],
        "Freeze 30s": ["freeze", "--timer", "30"],

        "Moonjump x1 (10s)": ["moon", "--level", "1", "--timer", "10"],
        "Moonjump x2 (30s)": ["moon", "--level", "2", "--timer", "30"],
        "Moonjump x3 (30s)": ["moon", "--level", "3", "--timer", "30"],
        "Moonjump OFF": ["moon", "--off"],

        "Camera lock ON": ["camera", "--on"],
        "Camera lock OFF": ["camera", "--off"],
        "Camera lock 10s": ["camera", "--timer", "10"],
        "Camera lock 30s": ["camera", "--timer", "30"],

        "Magic full": ["magic", "--full"],
        "Magic half": ["magic", "--half"],
        "Magic empty": ["magic", "--empty"],
        "Magic (choice)": ["__magic_choice__"],

        "Bombs emptied": ["bombs", "--empty"],
        "Bombs +5": ["bombs", "--add", "5"],
        "Arrows emptied": ["arrows", "--empty"],
        "Arrows +10": ["arrows", "--add", "10"],

        "Random item removed (10s)": ["item", "--random", "--timer", "10"],
        "Random item removed (30s)": ["item", "--random", "--timer", "30"],

        "Remove item (30s)": ["__item_remove__", "30"],
        "Remove item (60s)": ["__item_remove__", "60"]
    }
}

def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_tokens():
    if not TOKENS_PATH.exists():
        return None
    with TOKENS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_tokens(tokens):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with TOKENS_PATH.open("w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
