import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WW_ITEMS = BASE_DIR / "scripts" / "ww_items_ntscu.py"


def run_action(reward_title, user_input, config):
    mapping = config.get("rewards", {})
    reward_title = (reward_title or "").lower()
    args_cfg = None
    for name, args in mapping.items():
        if name.lower() == reward_title:
            args_cfg = args
            break
    if args_cfg is None:
        print("Reward non mappée:", reward_title)
        return
    if not WW_ITEMS.exists():
        print("ww_items_ntscu.py introuvable:", WW_ITEMS)
        return
    final_args = []
    for a in args_cfg:
        if a == "{input}":
            if user_input:
                final_args.append(str(user_input))
        else:
            final_args.append(str(a))
    creationflags = 0
    if sys.platform.startswith("win") and hasattr(subprocess, "CREATE_NO_WINDOW"):
        creationflags = subprocess.CREATE_NO_WINDOW
    cmd = [sys.executable, str(WW_ITEMS)] + final_args
    subprocess.Popen(cmd, creationflags=creationflags)
