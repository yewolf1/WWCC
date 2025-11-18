import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WW_ITEMS = BASE_DIR / "scripts" / "ww_items_ntscu.py"


def _norm(s):
    return (s or "").strip().lower()


def _resolve_time(user_input):
    key = _norm(user_input)
    mapping = {
        "day": ["time", "--day"],
        "jour": ["time", "--day"],
        "night": ["time", "--night"],
        "nuit": ["time", "--night"],
        "dawn": ["time", "--dawn"],
        "aube": ["time", "--dawn"],
        "dusk": ["time", "--dusk"],
        "crepuscule": ["time", "--dusk"],
        "crépuscule": ["time", "--dusk"],
        "cycle": ["time", "--cycle"],
    }
    if key in mapping:
        return mapping[key]
    try:
        value = float(user_input)
    except ValueError:
        return None
    return ["time", "--set", str(value)]


def _resolve_weather(user_input):
    key = _norm(user_input)
    mapping = {
        "clear": ["weather", "--clear"],
        "sun": ["weather", "--clear"],
        "soleil": ["weather", "--clear"],
        "cloudy": ["weather", "--cloudy"],
        "nuageux": ["weather", "--cloudy"],
        "rain": ["weather", "--rain"],
        "rainy": ["weather", "--rain"],
        "pluie": ["weather", "--rain"],
        "storm": ["weather", "--storm"],
        "orage": ["weather", "--storm"],
        "fog": ["weather", "--fog"],
        "brouillard": ["weather", "--fog"],
        "tempest": ["weather", "--tempest"],
        "tempete": ["weather", "--tempest"],
        "tempête": ["weather", "--tempest"],
        "cycle": ["weather", "--cycle"],
    }
    return mapping.get(key)


def _resolve_sword(user_input):
    key = _norm(user_input)
    if key in ("cycle", "c"):
        return ["sword", "--cycle"]
    aliases = {
        "off": "off",
        "none": "off",
        "hero": "hero",
        "ms1": "ms1",
        "ms2": "ms2",
        "ms3": "ms3",
        "0": "off",
        "1": "hero",
        "2": "ms1",
        "3": "ms2",
        "4": "ms3",
    }
    stage = aliases.get(key)
    if not stage:
        return None
    return ["sword", "--stage", stage]


def _resolve_shield(user_input):
    key = _norm(user_input)
    if key in ("cycle", "c"):
        return ["shield", "--cycle"]
    aliases = {
        "off": "off",
        "none": "off",
        "hero": "hero",
        "mirror": "mirror",
        "0": "off",
        "1": "hero",
        "2": "mirror",
    }
    stage = aliases.get(key)
    if not stage:
        return None
    return ["shield", "--stage", stage]


def _resolve_tunic(user_input):
    key = _norm(user_input)
    if key in ("cycle", "c"):
        return ["tunic", "--cycle"]
    aliases = {
        "green": "green",
        "verte": "green",
        "blue": "blue",
        "bleue": "blue",
        "0": "green",
        "1": "blue",
    }
    stage = aliases.get(key)
    if not stage:
        return None
    return ["tunic", "--stage", stage]

def _resolve_magic(user_input):
    key = _norm(user_input)

    # Mode cycle
    if key in ("cycle", "c"):
        return ["magic", "--cycle"]

    aliases = {
        "full": "full",
        "plein": "full",
        "max": "full",
        "100": "full",

        "half": "half",
        "moitie": "half",
        "moitié": "half",
        "50": "half",

        "empty": "empty",
        "vide": "empty",
        "0": "empty"
    }

    stage = aliases.get(key)
    if not stage:
        return None

    return ["magic", f"--{stage}"]


def _resolve_item_remove(args_cfg, user_input):
    raw = _norm(user_input)
    if not raw:
        return None

    # Normalisation : remplace espaces par underscores
    key = raw.replace(" ", "_")

    # Alias FR/EN → nom interne
    aliases = {
        # telescope
        "telescope": "telescope",
        "télescope": "telescope",

        # sail
        "sail": "sail",
        "voile": "sail",

        # wind waker
        "wind_waker": "wind_waker",
        "windwaker": "wind_waker",
        "baton_du_vent": "wind_waker",
        "bâton_du_vent": "wind_waker",

        # grappling_hook
        "grappling_hook": "grappling_hook",
        "grappin": "grappling_hook",

        # spoils_bag
        "spoils_bag": "spoils_bag",
        "sac_butin": "spoils_bag",
        "sac_de_butin": "spoils_bag",

        # boomerang
        "boomerang": "boomerang",
        "boomrang": "boomerang",
        "bomerang": "boomerang",

        # deku_leaf
        "deku_leaf": "deku_leaf",
        "feuille": "deku_leaf",
        "leaf": "deku_leaf",
        "feuille_deku": "deku_leaf",

        # tingle_tuner
        "tingle_tuner": "tingle_tuner",
        "tingle": "tingle_tuner",
        "tuner_tingle": "tingle_tuner",

        # pictobox
        "pictobox_dx": "pictobox_dx",
        "pictobox": "pictobox_dx",
        "appareil_photo": "pictobox_dx",

        # iron_boots
        "iron_boots": "iron_boots",
        "bottes_de_fer": "iron_boots",
        "bottes": "iron_boots",

        # magic armor
        "magic_armor": "magic_armor",
        "armure_magique": "magic_armor",

        # bait bag
        "bait_bag": "bait_bag",
        "sac_appats": "bait_bag",
        "sac_a_appats": "bait_bag",
        "appats": "bait_bag",
        "appâts": "bait_bag",

        # bow
        "bow": "bow",
        "arc": "bow",

        # fire & ice arrows
        "fire_ice_arrows": "fire_ice_arrows",
        "fire_ice": "fire_ice_arrows",
        "fleches_feu_glace": "fire_ice_arrows",
        "flèches_feu_glace": "fire_ice_arrows",

        # light arrows
        "light_arrows": "light_arrows",
        "fleches_lumiere": "light_arrows",
        "flèches_lumière": "light_arrows",

        # bombs
        "bombs": "bombs",
        "bombes": "bombs",

        # delivery bag
        "delivery_bag": "delivery_bag",
        "sac_de_livraison": "delivery_bag",

        # hookshot
        "hookshot": "hookshot",
        "grappin2": "hookshot",

        # skull hammer
        "skull_hammer": "skull_hammer",
        "marteau": "skull_hammer",
        "maillet": "skull_hammer",
    }

    # Traduction via alias FR/EN
    stage = aliases.get(key)
    if not stage:
        return None

    # Timer (30s ou 60s)
    seconds = 30
    if len(args_cfg) >= 2:
        try:
            seconds = int(args_cfg[1])
        except ValueError:
            seconds = 30

    # Commande finale
    return ["item", "--remove", stage, "--timer", str(seconds)]


def _build_args(args_cfg, reward_title, user_input):
    if not args_cfg:
        return None
    marker = args_cfg[0]
    if marker == "__time_choice__":
        return _resolve_time(user_input)
    if marker == "__weather_choice__":
        return _resolve_weather(user_input)
    if marker == "__sword_choice__":
        return _resolve_sword(user_input)
    if marker == "__shield_choice__":
        return _resolve_shield(user_input)
    if marker == "__tunic_choice__":
        return _resolve_tunic(user_input)
    if marker == "__item_remove__":
        return _resolve_item_remove(args_cfg, user_input)
    if marker == "__magic_choice__":
        return _resolve_magic(user_input)
    final = []
    for a in args_cfg:
        if a == "{input}":
            if user_input:
                final.append(str(user_input))
        else:
            final.append(str(a))
    return final


def run_action(reward_title, user_input, config):
    mapping = config.get("rewards", {})
    reward_title_l = (reward_title or "").lower()
    args_cfg = None
    for name, args in mapping.items():
        if name.lower() == reward_title_l:
            args_cfg = args
            break
    if args_cfg is None:
        print("Récompense non configurée:", reward_title)
        return
    final_args = _build_args(args_cfg, reward_title, user_input)
    if not final_args:
        print("Arguments invalides pour", reward_title, "/", user_input)
        return
    if not WW_ITEMS.exists():
        print("ww_items_ntscu.py introuvable:", WW_ITEMS)
        return
    creationflags = 0
    if sys.platform.startswith("win") and hasattr(subprocess, "CREATE_NO_WINDOW"):
        creationflags = subprocess.CREATE_NO_WINDOW
    cmd = [sys.executable, str(WW_ITEMS)] + final_args
    print("[CMD]", cmd)
    subprocess.Popen(cmd, creationflags=creationflags)
