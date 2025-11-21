import time
import struct
import sys
from dolphin_memory_engine import hook, write_bytes

# Great Sea Waves Modifier (Excluding Town Areas)
# 043E47D0 xxxxxxxx  ->  0x803E47D0 en RAM
WAVE_ADDR = 0x803E47D0

WAVE_LEVELS = {
    "off": 1.0,      
    "medium": 100.0,  
    "big": 400.0,   
    "freak": 1000.0,
    "apocalyptic": 10000.0
}

def apply_wave(mode):
    value = WAVE_LEVELS[mode]
    raw = struct.pack(">f", value)
    write_bytes(WAVE_ADDR, raw)

def main():
    hook()
    if len(sys.argv) < 2:
        raise SystemExit("Usage: ww_wave_lock.py <off|medium|big|freak|apocalyptic> [seconds]")

    mode = sys.argv[1]
    if mode not in WAVE_LEVELS:
        raise SystemExit("Mode invalide (off, medium, big, freak, apocalyptic)")

    if len(sys.argv) >= 3:
        seconds = int(sys.argv[2])
    else:
        seconds = 60

    end = time.time() + seconds
    while time.time() < end:
        apply_wave(mode)
        time.sleep(0.1)

    # On revient à des vagues normales (off = 1.0)
    if mode != "off":
        apply_wave("off")

if __name__ == "__main__":
    main()
