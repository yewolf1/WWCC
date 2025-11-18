import time
import sys
from dolphin_memory_engine import hook, write_bytes

CAMERA_FIXED_ADDR = 0x803C9EF4

def apply_camera_freeze():
    write_bytes(CAMERA_FIXED_ADDR, b"\x01")

def restore_camera():
    write_bytes(CAMERA_FIXED_ADDR, b"\x00")

def main():
    hook()
    seconds = int(sys.argv[1]) if len(sys.argv) >= 2 else 30
    end = time.time() + seconds
    while time.time() < end:
        apply_camera_freeze()
        time.sleep(0.05)
    restore_camera()

if __name__ == "__main__":
    main()
