import time
import struct
import sys
from dolphin_memory_engine import hook, write_bytes

# addr du jump :
JUMP_ADDR = 0x8035D4BC

LEVELS = {
    "1": 1.5,
    "2": 3.0,
    "3": 5.0,
}

def apply_jump(level):
    val = struct.pack(">f", LEVELS[level])
    write_bytes(JUMP_ADDR, val)

def main():
    hook()
    level = sys.argv[1]     # "1", "2", "3"
    seconds = int(sys.argv[2])

    end = time.time() + seconds

    while time.time() < end:
        apply_jump(level)
        time.sleep(0.05)

    apply_jump("1")  # retour au saut normal

if __name__ == "__main__":
    main()
