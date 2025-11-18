import time
from dolphin_memory_engine import hook, write_bytes
import sys
import time
import struct
import sys

FREEZE_SAFE_VAL = 0.0001

ADDR_DEFAULTS = {
    0x8035CEEC: 17.0,
    0x8035CF68: 12.0,
    0x8035CF98: 15.0,
    0x8035D548: 18.0,
    0x8035DB94: 3.0,
    0x8035DA3C: 30.0,
    0x8035DA60: 14.0,
    0x8035D410: 22.5,
    0x8035D414: 19.0,
    0x8035D28C: 18.0,
    0x8035D290: 27.0,
}

def apply_freeze():
    val = struct.pack(">f", float(FREEZE_SAFE_VAL))
    for addr in ADDR_DEFAULTS:
        write_bytes(addr, val)

def restore_defaults():
    for addr, default in ADDR_DEFAULTS.items():
        val = struct.pack(">f", float(default))
        write_bytes(addr, val)

def main():
    hook()
    duration = 30
    if len(sys.argv) >= 2:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            pass

    end = time.time() + duration
    while time.time() < end:
        apply_freeze()
        time.sleep(0.05)

    restore_defaults()

if __name__ == "__main__":
    main()

