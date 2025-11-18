import time
from dolphin_memory_engine import hook, write_bytes
import sys

# Usage: python ww_weather_lock.py rain
#        python ww_weather_lock.py storm

RAIN_ADDR      = 0x803E5474
SNOW_ADDR      = 0x803E5480
POLLEN_ADDR    = 0x803E54A8
LIGHTNING_ADDR = 0x803E54E8

def set(addr, level):
    write_bytes(addr, bytes([0,0,0,level]))

def apply_weather(mode):
    if mode == "clear":
        set(RAIN_ADDR, 0)
        set(SNOW_ADDR, 0)
        set(POLLEN_ADDR, 0)
        set(LIGHTNING_ADDR, 0)
    elif mode == "cloudy":
        set(RAIN_ADDR, 0)
        set(SNOW_ADDR, 0)
        set(POLLEN_ADDR, 0x20)
        set(LIGHTNING_ADDR, 0)
    elif mode == "rain":
        set(RAIN_ADDR, 0x80)
        set(SNOW_ADDR, 0)
        set(POLLEN_ADDR, 0)
        set(LIGHTNING_ADDR, 0)
    elif mode == "storm":
        set(RAIN_ADDR, 0xFA)
        set(SNOW_ADDR, 0)
        set(POLLEN_ADDR, 0)
        set(LIGHTNING_ADDR, 5)
    elif mode == "fog":
        set(RAIN_ADDR, 0)
        set(SNOW_ADDR, 0x80)
        set(POLLEN_ADDR, 0)
        set(LIGHTNING_ADDR, 0)
    elif mode == "tempest":
        set(RAIN_ADDR, 0xFA)
        set(SNOW_ADDR, 0x40)
        set(POLLEN_ADDR, 0x40)
        set(LIGHTNING_ADDR, 0x0A)

def main():
    hook()
    mode = sys.argv[1]

    end = time.time() + 60
    while time.time() < end:
        apply_weather(mode)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
