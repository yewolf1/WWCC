import time
import sys
from dolphin_memory_engine import hook, write_byte

# TABLE ITEMS (copiée depuis ton ww_items_ntscu, sans rien toucher)
ITEMS = {
    "telescope":      [(0x803C4C44, 0x20)],
    "sail":           [(0x803C4C45, 0x78)],
    "wind_waker":     [(0x803C4C46, 0x22)],
    "grappling_hook": [(0x803C4C47, 0x25)],
    "spoils_bag":     [(0x803C4C48, 0x24)],
    "boomerang":      [(0x803C4C49, 0x2D)],
    "deku_leaf":      [(0x803C4C4A, 0x34)],
    "tingle_tuner":   [(0x803C4C4B, 0x21)],
    "pictobox_dx":    [(0x803C4C4C, 0x26)],
    "iron_boots":     [(0x803C4C4D, 0x29)],
    "magic_armor":    [(0x803C4C4E, 0x2A)],
    "bait_bag":       [(0x803C4C4F, 0x2C)],
    "bow":            [(0x803C4C50, 0x27)],
    "fire_ice_arrows":[(0x803C4C50, 0x35)],
    "light_arrows":   [(0x803C4C50, 0x36)],
    "bombs":          [(0x803C4C51, 0x31)],
    "delivery_bag":   [(0x803C4C56, 0x30)],
    "hookshot":       [(0x803C4C57, 0x2F)],
    "skull_hammer":   [(0x803C4C58, 0x33)],
}

def remove_item(name):
    for addr, val in ITEMS[name]:
        write_byte(addr, 0x00)

def restore_item(name):
    for addr, val in ITEMS[name]:
        write_byte(addr, val)

def main():
    hook()

    item = sys.argv[1]
    seconds = int(sys.argv[2])

    remove_item(item)

    end = time.time() + seconds
    while time.time() < end:
        time.sleep(0.05)

    restore_item(item)

if __name__ == "__main__":
    main()
