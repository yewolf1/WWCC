import argparse
import random
import struct
import time
from dolphin_memory_engine import hook, write_byte, write_bytes, read_bytes
import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def script(path):
    return os.path.join(SCRIPT_DIR, path)

BASE = 0x80000000

ADDR = {
    "health_current": BASE + 0x003C4C0B,
    "equipped_item": BASE + 0x003C4C68,
    # "slot_b": 0x803CA7DA,
    "slot_y": 0x803CA7DC,
    "slot_x": 0x803CA7DB,
    "slot_z": 0x803CA7DD,
    "rupees" : BASE + 0x003C4C0C,
    "wallet" : BASE + 0x003C4C1A,
    "time" : BASE + 0x003C4C2C,
    "rain": 0x803E5474,
    "snow": 0x803E5480,
    "pollen": 0x803E54A8,
    "lightning": 0x803E54E8,
    "jump": BASE + 0x0035D4BC,
    "camera_fixed": BASE + 0x003C9EF4,
    "cam_manual": BASE + 0x00179238,
    "magic": BASE + 0x003C4C1C,
    "bombs":  BASE + 0x003C4C72,
    "arrows": BASE + 0x003C4C71,
    # "boat_moon": 0x80025170,
    # "boat_moon_on": 0xEC40102A,
    # "boat_moon_off": 0xEC401028, 
}

TIME_ORDER = [180.0, 285.0, 0.0, 105.0]

ITEMS = {
    "telescope":      [(BASE + 0x003C4C44, 0x20)],
    "sail":           [(BASE + 0x003C4C45, 0x78)],
    "wind_waker":     [(BASE + 0x003C4C46, 0x22)],
    "grappling_hook": [(BASE + 0x003C4C47, 0x25)],
    "spoils_bag":     [(BASE + 0x003C4C48, 0x24)],
    "boomerang":      [(BASE + 0x003C4C49, 0x2D)],
    "deku_leaf":      [(BASE + 0x003C4C4A, 0x34)],
    "tingle_tuner":   [(BASE + 0x003C4C4B, 0x21)],
    "pictobox_dx":    [(BASE + 0x003C4C4C, 0x26)],
    "iron_boots":     [(BASE + 0x003C4C4D, 0x29)],
    "magic_armor":    [(BASE + 0x003C4C4E, 0x2A)],
    "bait_bag":       [(BASE + 0x003C4C4F, 0x2C)],
    "bow":            [(BASE + 0x003C4C50, 0x27)],
    "fire_ice_arrows":[(BASE + 0x003C4C50, 0x35)],
    "light_arrows":   [(BASE + 0x003C4C50, 0x36)],
    "bombs":          [(BASE + 0x003C4C51, 0x31)],
    "delivery_bag":   [(BASE + 0x003C4C56, 0x30)],
    "hookshot":       [(BASE + 0x003C4C57, 0x2F)],
    "skull_hammer":   [(BASE + 0x003C4C58, 0x33)],
}

SWORD_STAGES = {
    "off": [
        (BASE + 0x003C4C16, 0xFF),
        (BASE + 0x003C4CBC, 0x00),
    ],
    "hero": [
        (BASE + 0x003C4C16, 0x38),
        (BASE + 0x003C4CBC, 0x01),
    ],
    "ms1": [
        (BASE + 0x003C4C16, 0x39),
        (BASE + 0x003C4CBC, 0x03),
    ],
    "ms2": [
        (BASE + 0x003C4C16, 0x3A),
        (BASE + 0x003C4CBC, 0x07),
    ],
    "ms3": [
        (BASE + 0x003C4C16, 0x3E),
        (BASE + 0x003C4CBC, 0x0F),
    ],
}

SWORD_ORDER = ["off", "hero", "ms1", "ms2", "ms3"]

SHIELD_STAGES = {
    "off": [
        (BASE + 0x003C4C17, 0xFF),
        (BASE + 0x003C4CBD, 0x00),
    ],
    "hero": [
        (BASE + 0x003C4C17, 0x3B),
        (BASE + 0x003C4CBD, 0x01),
    ],
    "mirror": [
        (BASE + 0x003C4C17, 0x3C),
        (BASE + 0x003C4CBD, 0x03),
    ],
}

SHIELD_ORDER = ["off", "hero", "mirror"]

TUNIC_STAGES = {
    "green": [
        (BASE + 0x003C4DA8, 0x00),
        (BASE + 0x003C4E11, 0x00),
    ],
    "blue": [
        (BASE + 0x003C4DA8, 0x01),
        (BASE + 0x003C4E11, 0x01),
    ],
}

TUNIC_ORDER = ["green", "blue"]

FREEZE_SAFE_VAL = 0.0001

FREEZE_ADDRS_DEFAULTS = {
    0x8035CEEC: 17.0,   # normal speed
    0x8035CF68: 12.0,   # lock-on F/L/R speed
    0x8035CF98: 15.0,   # lock-on back speed
    0x8035D548: 18.0,   # swim speed
    0x8035DB94: 3.0,    # crawl speed
    0x8035DA3C: 30.0,   # sidestep speed
    0x8035DA60: 14.0,   # sidestep height
    0x8035D410: 22.5,   # backflip speed
    0x8035D414: 19.0,   # backflip height
    0x8035D28C: 18.0,   # jump slash speed
    0x8035D290: 27.0,   # jump slash height
}

WAVE_ADDR = 0x803E47D0
WAVE_LEVELS = {
    "off": 1.0,      
    "medium": 100.0,  
    "big": 400.0,   
    "freak": 1000.0,
    "apocalyptic": 10000.0
}

#######################################################################
# HELPERS
#######################################################################

def ensure():
    """Vérifie que Dolphin est bien accessible."""
    hook()
    try:
        read_bytes(BASE, 1)
    except Exception:
        raise SystemExit("Dolphin non détecté ou jeu non en cours.")
    

#######################################################################
# ITEM WRITE
#######################################################################

def write_on(entries, enable=True):
    ensure()
    for addr, val in entries:
        write_byte(addr, val if enable else 0x00)
        
def set_time_float(value):
    ensure()
    if value < 0:
        value = 0.0
    if value > 360:
        value = 360.0
    data = struct.pack(">f", float(value))
    write_bytes(ADDR["time"], data)
    return value

#######################################################################
# SWORD AND SHEILD
#######################################################################

def apply_sword_stage(stage):
    for addr, val in SWORD_STAGES[stage]:
        write_byte(addr, val)

def detect_current_sword():
    inv = read_bytes(BASE + 0x003C4C16, 1)[0]
    b   = read_bytes(BASE + 0x003C4CBC, 1)[0]

    for name, values in SWORD_STAGES.items():
        inv_addr, inv_val = values[0]
        b_addr, b_val     = values[1]
        if inv_val == inv and b_val == b:
            return name

    return "off"

def detect_current_shield():
    inv = read_bytes(BASE + 0x003C4C17, 1)[0]
    b   = read_bytes(BASE + 0x003C4CBD, 1)[0]

    for name, values in SHIELD_STAGES.items():
        inv_addr, inv_val = values[0]
        b_addr, b_val     = values[1]
        if inv_val == inv and b_val == b:
            return name

    return "off"

def apply_shield_stage(stage):
    for addr, val in SHIELD_STAGES[stage]:
        write_byte(addr, val)
        
#######################################################################
# TUNIC
#######################################################################
        
def detect_current_tunic():
    valA = read_bytes(BASE + 0x003C4DA8, 1)[0]
    valB = read_bytes(BASE + 0x003C4E11, 1)[0]

    for name, values in TUNIC_STAGES.items():
        a_addr, a_val = values[0]
        b_addr, b_val = values[1]
        if valA == a_val and valB == b_val:
            return name

    return "green"
        
def apply_tunic_stage(stage):
    for addr, val in TUNIC_STAGES[stage]:
        write_byte(addr, val)
        
#######################################################################
# RUPEES
#######################################################################
        
def get_rupees():
    ensure()
    data = read_bytes(ADDR["rupees"], 2)
    return (data[0] << 8) | data[1]

def set_rupees(value):
    ensure()
    if value < 0:
        value = 0
    if value > 9999:
        value = 9999
    hi = (value >> 8) & 0xFF
    lo = value & 0xFF
    write_byte(ADDR["rupees"], hi)
    write_byte(ADDR["rupees"] + 1, lo)
    return get_rupees()

def get_wallet_tier():
    ensure()
    val = read_bytes(ADDR["wallet"], 1)[0]
    if val not in (0, 1, 2):
        return 0
    return val

def get_wallet_max():
    tier = get_wallet_tier()
    if tier == 0:
        return 500
    elif tier == 1:
        return 1000
    return 5000

def add_rupees(delta):
    current = get_rupees()
    return set_rupees(current + delta)

#######################################################################
# WEATHER (avec chemins corrigés)
#######################################################################

def launch_weather(mode):
    subprocess.Popen([
        sys.executable,        
        script("ww_weather_lock.py"), 
        mode                   
    ])
    print(f"Météo '{mode}' lancée pendant 60s (en arrière-plan).")
    
#######################################################################
# FREEZE 
#######################################################################
    
def apply_freeze_movement():
    ensure()
    val = struct.pack(">f", float(FREEZE_SAFE_VAL))
    for addr in FREEZE_ADDRS_DEFAULTS:
        write_bytes(addr, val)
    print("Freeze mouvement : ON")

def restore_movement_defaults():
    ensure()
    for addr, default in FREEZE_ADDRS_DEFAULTS.items():
        val = struct.pack(">f", float(default))
        write_bytes(addr, val)
    print("Freeze mouvement : OFF (valeurs restaurées)")

def launch_freeze_timer(seconds):
    subprocess.Popen([
        sys.executable,
        script("ww_freeze_lock.py"),
        str(seconds)
    ])
    print(f"Freeze mouvement lancé pendant {seconds}s (en arrière-plan).")
    
#######################################################################
# WAVES
#######################################################################

def set_wave(mode):
    ensure()
    if mode not in WAVE_LEVELS:
        raise SystemExit("Mode de vagues invalide (off, medium, big, freak)")
    val = struct.pack(">f", WAVE_LEVELS[mode])
    write_bytes(WAVE_ADDR, val)
    print(f"Vagues: {mode} (max={WAVE_LEVELS[mode]})")

def launch_waves_timer(mode, seconds):
    subprocess.Popen([
        sys.executable,
        script("ww_wave_lock.py"),
        mode,
        str(int(seconds)),
    ])
    print(f"Vagues '{mode}' pendant {seconds}s (en arrière-plan).")
    
#######################################################################
# MOONJUMP
#######################################################################
    
def moon_set_level(level):
    # niveaux : 1=normal, 2=moon léger, 3=moon fort
    LEVEL_MAP = {
        1: 1.5,
        2: 3.0,
        3: 5.0,
    }
    if level not in LEVEL_MAP:
        raise SystemExit("Niveau invalide. Choisis : 1, 2, 3")

    val = struct.pack(">f", LEVEL_MAP[level])
    write_bytes(ADDR["jump"], val)
    print(f"Moonjump niveau {level} -> valeur {LEVEL_MAP[level]}")
    
def launch_moon_timer(level, seconds):
    subprocess.Popen([
        sys.executable,
        script("ww_moon_lock.py"),
        str(level),
        str(seconds),
    ])
    print(f"Moonjump niveau {level} pendant {seconds}s (en arrière-plan).")

#######################################################################
# CAMERA
#######################################################################
  
def apply_camera_freeze():
    ensure()
    write_bytes(ADDR["camera_fixed"], b"\x01")

def restore_camera():
    ensure()
    write_bytes(ADDR["camera_fixed"], b"\x00")

def launch_camera_timer(seconds):
    subprocess.Popen([
        sys.executable,
        script("ww_camera_lock.py"),
        str(int(seconds)),
    ])

#######################################################################
# MAGIC
#######################################################################
   
def get_magic():
    ensure()
    return read_bytes(ADDR["magic"], 1)[0]

def set_magic(value):
    ensure()
    if value < 0:
        value = 0
    if value > 32:
        value = 32
    write_byte(ADDR["magic"], value)
    return get_magic()

def get_magic_max():
    ensure()
    cur = get_magic()

    if cur > 16:
        return 32
    elif cur > 0 and cur > 15:
        return 16
    else:
        return 32

#######################################################################
# Bombs
#######################################################################
   
def get_bombs():
    ensure()
    return read_bytes(ADDR["bombs"], 1)[0]

def set_bombs(value):
    ensure()
    if value < 0:
        value = 0
    if value > 255:
        value = 255
    write_byte(ADDR["bombs"], value)
    return get_bombs()

def add_bombs(amount):
    ensure()
    current = get_bombs()
    new_val = current + amount
    if new_val > 99:
        new_val = 99
    if new_val < 0:
        new_val = 0
    write_byte(ADDR["bombs"], new_val)
    return new_val

#######################################################################
# ARROWS
#######################################################################

def get_arrows():
    ensure()
    return read_bytes(ADDR["arrows"], 1)[0]

def set_arrows(value):
    ensure()
    if value < 0:
        value = 0
    if value > 255:
        value = 255
    write_byte(ADDR["arrows"], value)
    return get_arrows()

def add_arrows(amount):
    ensure()
    current = get_arrows()
    new_val = current + amount
    if new_val > 99:
        new_val = 99
    if new_val < 0:
        new_val = 0
    write_byte(ADDR["arrows"], new_val)
    return new_val

#######################################################################
# HEARTS
#######################################################################

def set_hearts(hearts):
    ensure()
    quarters = int(hearts * 4)
    if quarters < 0:
        quarters = 0
    if quarters > 0xFF:
        quarters = 0xFF
    write_byte(ADDR["health_current"], quarters)
    return quarters

#######################################################################
# BOAT MOONJUMP
#######################################################################

def boat_moon_write(val):
    ensure()
    write_bytes(ADDR["boat_moon"], val.to_bytes(4, "big"))

def boat_moon_on():
    boat_moon_write(ADDR["boat_moon_on"])
    print("Moonjump bateau : ON")

def boat_moon_off():
    boat_moon_write(ADDR["boat_moon_off"])
    print("Moonjump bateau : OFF")

def launch_boat_moon_timer(seconds):
    subprocess.Popen([
        sys.executable,
        script("ww_boat_moon_lock.py"),
        str(int(seconds)),
    ])
    print(f"Moonjump bateau pendant {seconds}s (en arrière-plan).")

    
#######################################################################
# CMD METHODS
#######################################################################

def cmd_waves(mode=None, timer=None):
    if timer is not None:
        launch_waves_timer(mode, timer)
    elif mode is not None:
        set_wave(mode)

def cmd_hp_quarter():
    q = set_hearts(0.25)
    print(f"Sante reglee a 1/4 de coeur ({q} quarts)")


def cmd_hp_three():
    q = set_hearts(3)
    print(f"Sante reglee a 3 coeurs ({q} quarts)")


def cmd_hp_set(hearts):
    q = set_hearts(hearts)
    print(f"Sante reglee a {hearts} coeurs ({q} quarts)")

def cmd_item_remove_timer(item, seconds):
    subprocess.Popen([
        sys.executable,
        script("ww_item_lock.py"),
        item,
        str(int(seconds)),
    ])
    print(f"Item {item} retiré pendant {seconds} secondes.")
    
def cmd_item_random_timer(seconds):
    item = random.choice(list(ITEMS.keys()))
    print(f"Item aléatoire choisi : {item} (retiré pendant {seconds} secondes)")

    subprocess.Popen([
        sys.executable,
        script("ww_item_lock.py"),
        item,
        str(int(seconds)),
    ])

def cmd_bombs_empty():
    before = get_bombs()
    after = set_bombs(0)
    print(f"Bombes : {before} -> {after}")

def cmd_bombs_add(amount):
    before = get_bombs()
    after = add_bombs(amount)
    print(f"Bombes : {before} -> {after}")

def cmd_arrows_empty():
    before = get_arrows()
    after = set_arrows(0)
    print(f"Flèches : {before} -> {after}")

def cmd_arrows_add(amount):
    before = get_arrows()
    after = add_arrows(amount)
    print(f"Flèches : {before} -> {after}")

def cmd_magic_full():
    max_val = get_magic_max()
    new_val = set_magic(max_val)
    print(f"Magie full ({new_val}/{max_val})")

def cmd_magic_half():
    max_val = get_magic_max()
    current = get_magic()
    new_val = set_magic(current // 2)
    print(f"Magie half : {current} -> {new_val} (max={max_val})")

def cmd_magic_empty():
    new_val = set_magic(0)
    print("Magie vide (0)")

def cmd_camera(on=False, off=False, timer=None):
    if on:
        apply_camera_freeze()
        print("Caméra figée (ON).")
    elif off:
        restore_camera()
        print("Caméra restaurée (OFF).")
    elif timer is not None:
        launch_camera_timer(timer)

def cmd_moon(level=None, timer=None, off=False, boat=False):
    ensure()

    # Mode spécial bateau
    if boat:
        if off:
            boat_moon_off()
            return
        if timer is not None:
            launch_boat_moon_timer(timer)
            return
        boat_moon_on()
        return

    # Mode normal (Link)
    if off:
        val = struct.pack(">f", 1.5)
        write_bytes(ADDR["jump"], val)
        print("Moonjump OFF (saut normal)")
        return

    if timer is not None:
        launch_moon_timer(level, timer)
        return

    if level is not None:
        moon_set_level(level)

def cmd_freeze(on=False, off=False, timer=None):
    if on:
        apply_freeze_movement()
    elif off:
        restore_movement_defaults()
    elif timer is not None:
        launch_freeze_timer(timer)

def cmd_add(name):
    if name not in ITEMS:
        raise SystemExit(f"Item inconnu: {name}")
    write_on(ITEMS[name], True)
    print(f"Ajouté: {name}")

def cmd_remove(name):
    if name not in ITEMS:
        raise SystemExit(f"Item inconnu: {name}")
    write_on(ITEMS[name], False)
    print(f"Retiré: {name}")

def cmd_kill():
    ensure()
    write_byte(ADDR["health_current"], 0x00)
    print("PV = 0")

def cmd_sword(stage=None, cycle=False):
    ensure()

    if cycle:
        current = detect_current_sword()
        idx = SWORD_ORDER.index(current)
        next_stage = SWORD_ORDER[(idx + 1) % len(SWORD_ORDER)]
        apply_sword_stage(next_stage)
        print(f"Cycle épée : {current} -> {next_stage}")
        return

    if stage not in SWORD_STAGES:
        raise SystemExit("Choisis : off, hero, ms1, ms2, ms3, ou --cycle")

    apply_sword_stage(stage)
    print(f"Épée définie sur : {stage}")
    
def cmd_shield(stage=None, cycle=False):
    ensure()

    if cycle:
        current = detect_current_shield()
        idx = SHIELD_ORDER.index(current)
        next_stage = SHIELD_ORDER[(idx + 1) % len(SHIELD_ORDER)]
        apply_shield_stage(next_stage)
        print(f"Cycle bouclier : {current} -> {next_stage}")
        return

    if stage not in SHIELD_STAGES:
        raise SystemExit("Choisis : off, hero, mirror, ou --cycle")

    apply_shield_stage(stage)
    print(f"Bouclier défini sur : {stage}")

def cmd_unequip(slot, all_slots=False):
    ensure()
    if all_slots:
        write_byte(ADDR["slot_y"], 0xff)
        write_byte(ADDR["slot_x"], 0xff)
        write_byte(ADDR["slot_z"], 0xff)
        print("Slots X, Y, Z déséquipés.")
        return

    slot = slot.lower()
    if slot == "x":
        write_byte(ADDR["slot_x"], 0xff)
        print("Slot X déséquipé.")
    elif slot == "y":
        write_byte(ADDR["slot_y"], 0xff)
        print("Slot Y déséquipé.")
    elif slot == "z":
        write_byte(ADDR["slot_z"], 0xff)
        print("Slot Z déséquipé.")
    else:
        raise SystemExit("Slot invalide. Choisis : x, y, z, ou --all.")
    
def cmd_tunic(stage=None, cycle=False):
    ensure()

    if cycle:
        current = detect_current_tunic()
        idx = TUNIC_ORDER.index(current)
        next_stage = TUNIC_ORDER[(idx + 1) % len(TUNIC_ORDER)]
        apply_tunic_stage(next_stage)
        print(f"Tunique cyclée : {current} -> {next_stage}")
        return

    if stage not in TUNIC_STAGES:
        raise SystemExit("Choisis : green, blue, ou --cycle")

    apply_tunic_stage(stage)
    print(f"Tunique définie : {stage}")


def cmd_rupees_get():
    val = get_rupees()
    print(f"Rubis actuels : {val}")

def cmd_rupees_set(value):
    new_val = set_rupees(value)
    print(f"Rubis définis sur : {new_val}")

def cmd_rupees_add(delta):
    new_val = add_rupees(delta)
    print(f"Rubis après ajout : {new_val}")

def cmd_wallet_cycle():
    current = get_wallet_tier()
    nxt = (current + 1) % 3
    write_byte(ADDR["wallet"], nxt)
    print(f"Wallet cycle : {current} -> {nxt}")
    
def cmd_wallet_set(tier):
    ensure()
    write_byte(ADDR["wallet"], tier)
    print(f"Wallet définie sur tier {tier}")

def cmd_wallet_cycle():
    current = get_wallet_tier()
    nxt = (current + 1) % 3
    write_byte(ADDR["wallet"], nxt)
    print(f"Wallet cycle : {current} -> {nxt}")
    
def cmd_rupees_random():
    max_val = get_wallet_max()
    value = random.randint(0, max_val)
    new_val = set_rupees(value)
    print(f"Rubis aléatoires (max {max_val}) : {new_val}")

def cmd_rupees_half():
    current = get_rupees()
    new_val = set_rupees(current // 2)
    print(f"Rubis divisés par 2 : {new_val}")

def cmd_rupees_double():
    current = get_rupees()
    new_val = set_rupees(min(current * 2, 9999))
    print(f"Rubis doublés : {new_val}")
    
def cmd_time_day():
    set_time_float(180.0)
    print("Temps réglé sur JOUR (12:00)")

def cmd_time_night():
    set_time_float(0.0)
    print("Temps réglé sur NUIT (00:00)")

def cmd_time_dawn():
    set_time_float(105.0)
    print("Temps réglé sur AUBE (07:00)")

def cmd_time_dusk():
    set_time_float(285.0)
    print("Temps réglé sur CRÉPUSCULE (19:00)")

def cmd_time_set(value):
    set_time_float(value)
    print(f"Temps réglé sur {value}°")

def cmd_time_cycle():
    ensure()
    cur_bytes = read_bytes(ADDR["time"], 4)
    cur = struct.unpack(">f", cur_bytes)[0]
    distances = [(abs(cur - t), t) for t in TIME_ORDER]
    _, nearest = min(distances)
    idx = TIME_ORDER.index(nearest)
    nxt = TIME_ORDER[(idx + 1) % len(TIME_ORDER)]
    set_time_float(nxt)
    print(f"Cycle temps : {nearest}° -> {nxt}°")
    
def cmd_weather_clear():
    launch_weather("clear")

def cmd_weather_cloudy():
    launch_weather("cloudy")

def cmd_weather_rain():
    launch_weather("rain")

def cmd_weather_storm():
    launch_weather("storm")

def cmd_weather_fog():
    launch_weather("fog")

def cmd_weather_tempest():
    launch_weather("tempest")

def cmd_weather_cycle():
    ensure()
    r = read_bytes(ADDR["rain"], 4)[3]
    s = read_bytes(ADDR["snow"], 4)[3]
    p = read_bytes(ADDR["pollen"], 4)[3]
    l = read_bytes(ADDR["lightning"], 4)[3]

    if r == 0 and s == 0 and p == 0 and l == 0:
        cmd_weather_rain()
    elif r >= 0x80 and l == 0:
        cmd_weather_storm()
    elif r >= 0x80 and l > 0:
        cmd_weather_fog()
    elif s >= 0x40 and r == 0:
        cmd_weather_tempest()
    else:
        cmd_weather_clear()

#######################################################################
# MAIN PROCESS
#######################################################################

def main():
    p = argparse.ArgumentParser(description="Wind Waker NTSC-U (GZLE01) items + options")
    sub = p.add_subparsers(dest="cmd", required=True)
    
    p_item = sub.add_parser("item")
    group_item = p_item.add_mutually_exclusive_group(required=True)
    group_item.add_argument("--add")
    group_item.add_argument("--remove")
    group_item.add_argument("--random", action="store_true")
    p_item.add_argument("--timer", type=int)

    sub.add_parser("kill")
    sub.add_parser("list")
    
    p_uneq = sub.add_parser("unequip")
    p_uneq.add_argument("--slot", choices=["x","y","z"], required=False)
    p_uneq.add_argument("--all", action="store_true")
    
    p_sword = sub.add_parser("sword")
    p_sword.add_argument("--stage", choices=["off","hero","ms1","ms2","ms3"])
    p_sword.add_argument("--cycle", action="store_true")
    
    p_shield = sub.add_parser("shield")
    p_shield.add_argument("--stage", choices=["off","hero","mirror"])
    p_shield.add_argument("--cycle", action="store_true")
    
    p_tunic = sub.add_parser("tunic")
    p_tunic.add_argument("--stage", choices=["green","blue"])
    p_tunic.add_argument("--cycle", action="store_true")
    
    p_rupees = sub.add_parser("rupees")
    group = p_rupees.add_mutually_exclusive_group(required=True)
    group.add_argument("--get", action="store_true")
    group.add_argument("--set", type=int)
    group.add_argument("--add", type=int)
    
    p_wallet = sub.add_parser("wallet")
    group_w = p_wallet.add_mutually_exclusive_group(required=True)
    group_w.add_argument("--tier", type=int, choices=[0, 1, 2])
    group_w.add_argument("--cycle", action="store_true")
    
    p_time = sub.add_parser("time")
    group_t = p_time.add_mutually_exclusive_group(required=True)
    group_t.add_argument("--day", action="store_true")
    group_t.add_argument("--night", action="store_true")
    group_t.add_argument("--dawn", action="store_true")
    group_t.add_argument("--dusk", action="store_true")
    group_t.add_argument("--cycle", action="store_true")
    group_t.add_argument("--set", type=float)
    
    p_weather = sub.add_parser("weather")
    group_wth = p_weather.add_mutually_exclusive_group(required=True)
    group_wth.add_argument("--clear", action="store_true")
    group_wth.add_argument("--cloudy", action="store_true")
    group_wth.add_argument("--rain", action="store_true")
    group_wth.add_argument("--storm", action="store_true")
    group_wth.add_argument("--fog", action="store_true")
    group_wth.add_argument("--tempest", action="store_true")
    group_wth.add_argument("--cycle", action="store_true")
    
    p_freeze = sub.add_parser("freeze")
    group_f = p_freeze.add_mutually_exclusive_group(required=True)
    group_f.add_argument("--on", action="store_true")
    group_f.add_argument("--off", action="store_true")
    group_f.add_argument("--timer", type=int)
    
    p_moon = sub.add_parser("moon")
    p_moon.add_argument("--level", type=int, choices=[1, 2, 3])
    p_moon.add_argument("--timer", type=int)
    p_moon.add_argument("--off", action="store_true")
    # p_moon.add_argument("--boat", action="store_true")
    
    p_camera = sub.add_parser("camera")
    group_cam = p_camera.add_mutually_exclusive_group(required=True)
    group_cam.add_argument("--on", action="store_true")
    group_cam.add_argument("--off", action="store_true")
    group_cam.add_argument("--timer", type=int)
    
    p_magic = sub.add_parser("magic")
    group_magic = p_magic.add_mutually_exclusive_group(required=True)
    group_magic.add_argument("--full", action="store_true")
    group_magic.add_argument("--half", action="store_true")
    group_magic.add_argument("--empty", action="store_true")

    p_bombs = sub.add_parser("bombs")
    p_bombs.add_argument("--empty", action="store_true")
    p_bombs.add_argument("--add", type=int)

    p_arrows = sub.add_parser("arrows")
    p_arrows.add_argument("--empty", action="store_true")
    p_arrows.add_argument("--add", type=int)
    
    p_hp = sub.add_parser("hp")
    group_hp = p_hp.add_mutually_exclusive_group(required=True)
    group_hp.add_argument("--quarter", action="store_true")
    group_hp.add_argument("--three", action="store_true")
    group_hp.add_argument("--set", type=float)
    
    p_waves = sub.add_parser("waves")
    p_waves.add_argument("--mode", choices=["off", "medium", "big", "freak","apocalyptic"], required=True)
    p_waves.add_argument("--timer", type=int)


    a = p.parse_args()
    if a.cmd == "kill":
        cmd_kill()
    elif a.cmd == "list":
        for k in sorted(ITEMS):
            print(k)
    elif a.cmd == "sword":
        cmd_sword(a.stage, a.cycle)
    elif a.cmd == "shield":
        cmd_shield(a.stage, a.cycle)
    elif a.cmd == "unequip":
        cmd_unequip(a.slot, a.all)
    elif a.cmd == "tunic":
        cmd_tunic(a.stage, a.cycle)
    elif a.cmd == "rupees":
        if a.get:
            cmd_rupees_get()
        elif a.set is not None:
            cmd_rupees_set(a.set)
        elif a.add is not None:
            cmd_rupees_add(a.add)
    elif a.cmd == "wallet":
        if getattr(a, "cycle", False):
            cmd_wallet_cycle()
        else:
            cmd_wallet_set(a.tier)
    elif a.cmd == "time":
        if a.day:
            cmd_time_day()
        elif a.night:
            cmd_time_night()
        elif a.dawn:
            cmd_time_dawn()
        elif a.dusk:
            cmd_time_dusk()
        elif a.cycle:
            cmd_time_cycle()
        elif a.set is not None:
            cmd_time_set(a.set)
    elif a.cmd == "weather":
        if a.clear:
            cmd_weather_clear()
        elif a.cloudy:
            cmd_weather_cloudy()
        elif a.rain:
            cmd_weather_rain()
        elif a.storm:
            cmd_weather_storm()
        elif a.fog:
            cmd_weather_fog()
        elif a.tempest:
            cmd_weather_tempest()
        elif a.cycle:
            cmd_weather_cycle()
    elif a.cmd == "freeze":
        cmd_freeze(a.on, a.off, a.timer)
    elif a.cmd == "moon":
        cmd_moon(level=a.level, timer=a.timer, off=a.off)
    elif a.cmd == "camera":
        cmd_camera(on=a.on, off=a.off, timer=a.timer)
    elif a.cmd == "magic":
        if a.full:
            cmd_magic_full()
        elif a.half:
            cmd_magic_half()
        elif a.empty:
            cmd_magic_empty()
    elif a.cmd == "bombs":
        if a.empty:
            cmd_bombs_empty()
        elif a.add is not None:
            cmd_bombs_add(a.add)

    elif a.cmd == "arrows":
        if a.empty:
            cmd_arrows_empty()
        elif a.add is not None:
            cmd_arrows_add(a.add)
    elif a.cmd == "item":
        if a.add:
            cmd_add(a.add)

        elif a.remove and a.timer:
            cmd_item_remove_timer(a.remove, a.timer)

        elif a.remove:
            cmd_remove(a.remove)

        elif a.random and a.timer:
            cmd_item_random_timer(a.timer)

        elif a.random:
            print("La commande --random nécessite --timer X")    
    elif a.cmd == "hp":
        if a.quarter:
            cmd_hp_quarter()
        elif a.three:
            cmd_hp_three()
        elif a.set is not None:
            cmd_hp_set(a.set)
    elif a.cmd == "waves":
        cmd_waves(mode=a.mode, timer=a.timer)
        
if __name__ == "__main__":
    main()
