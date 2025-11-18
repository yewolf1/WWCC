# 🌪️ Wind Waker Chaotic Controller  
A real‑time controller for **The Legend of Zelda: The Wind Waker (NTSC‑U – GZLE01)** using **Dolphin Emulator**, with optional **Twitch Channel Points integration**.  

---

# ✨ Features Overview

## 🎮 Real‑Time Game Control
- Add / remove / temporarily disable items  
- Unequip item slots X / Y / Z  
- Change sword, shield and tunic levels  
- Modify rupees, magic, bombs, arrows  
- Freeze movement, fix the camera, moonjump levels  
- Change in‑game time, force or cycle weather  
- Kill Link, heart presets, advanced heart slider  


## 🔗 Twitch Channel Points Integration
- Viewers trigger effects directly in your game  
- Full mapping of Twitch rewards → commands  
- Works in background, non‑blocking  

---

# 📦 Installation Guide

## ✔ Requirements
- **Windows 10/11**  
- **Dolphin Emulator** (stable or MMJR recommended)  
- **Wind Waker NTSC‑U (GZLE01) (not sure that will work on other NTSC‑U ver)**  
- Portable Python **already included** → no installation required  

---

# 📁 Project Structure

```
WWCC/
 ├─ assets/                   # UI icons, images
 ├─ python/                   # Embedded portable Python runtime
 ├─ scripts/                  # External effect scripts (weather, freeze, etc.)
 │   ├─ check_dolphin.py
 │   ├─ ww_camera_lock.py
 │   ├─ ww_controller_ui.py
 │   ├─ ww_freeze_lock.py
 │   ├─ ww_item_lock.py
 │   ├─ ww_items_ntscu.py     # Main game memory interaction engine
 │   ├─ ww_locale.py
 │   ├─ ww_moon_lock.py
 │   └─ ww_weather_lock.py
 │
 ├─ twitch_controller/        # Twitch integration logic
 │   ├─ __init__.py
 │   ├─ actions.py
 │   ├─ config.py
 │   └─ main.py
 │
 ├─ ww_controller_ui.exe      # Compiled application (to place at root)
```

---

# ▶️ Running the Application

### 🟦 Development (using embedded python)
```
.\python\python.exe ww_controller_ui.py
```

### 🟩 Packaged version
```
ww_controller_ui.exe
```

---

# 🔧 Twitch Setup (Full Step‑by‑Step Guide)

To allow channel point rewards to trigger game effects, you must configure a **Twitch Developer Application**, and create a `.env` file.

---

## 1️⃣ Create a Twitch Developer Application (DETAILED)

Go to:  
👉 https://dev.twitch.tv/console/apps

Click **Create Application**, then fill these fields:

| Field | Value |
|-------|--------|
| Name | WindWakerController |
| OAuth Redirect URL | `http://localhost:17563` |
| Category | Application Integration |


Your app uses this URL internally when reconnecting to Twitch.

### After creation, note:
- **Client ID**  
- **Client Secret**  
Never share the Secret publicly.

---

## 2️⃣ Configure the `.env` File

Create or edit the `.env` file at the project root:

```
TWITCH_CLIENT_ID=your_client_id
TWITCH_CLIENT_SECRET=your_client_secret
```

This file MUST exist before connecting.

---

## 3️⃣ Create Channel Point Rewards in Twitch

Go to:  
**Creator Dashboard → Viewer Rewards → Channel Points → Manage Rewards**

Create rewards that match your configuration.

Example recommended setup:

| Reward Name | Trigger |
|-------------|---------|
| Kill Link | kill |
| 1/4 heart | hp --quarter |
| 3 hearts | hp --three |
| Unequip X | unequip --slot x |
| Unequip Y | unequip --slot y |
| Unequip Z | unequip --slot z |
| Unequip all | unequip --all |
| Sword: Cycle | sword --cycle |
| Sword: Off | sword --stage off |
| Moonjump Lvl 2 (30s) | moon --level 2 --timer 30 |

You can add many more (weather, random items, camera lock…).
All the default config is on the file -> /twitch_controller/config.py

---

## 4️⃣ Connect the App to Twitch

1. Open the application  
2. Go to **Twitch Controller**  
3. Click **Connect**  
4. A Twitch login window appears  
5. Approve access  

If everything works, you'll see:

```
Connected To Twitch !
Listening for channel point redemptions...
```

---

# 🎛️ Using the Controller

### Items  
Add/remove, timed removal, random removal.

### Equipment  
Sword levels, shield levels, tunic colors, slot unequip.

### Resources  
Rupees, wallet tier, bombs, arrows, magic.

### Time & Weather  
Day/night, dawn/dusk, cycle, fog/rain/storm/tempest, etc.

### Effects  
Movement freeze, moonjump (levels + timer), camera lock.

### System  
Kill Link, hearts, utilities, item list.

---

# 🧪 Troubleshooting

### 🔍 Dolphin is not detected
Run:
```
.\python\python.exe check_dolphin.py
```

Ensure:
- Dolphin is open  
- The ROM is NTSC‑U (GZLE01)  
- The game is running  

---

# 📦 Building a New .EXE (Useful for users having issues)

If you need to generate a fresh executable:

```
.\python\python.exe -m PyInstaller ww_controller_ui.spec
```

After building, your new EXE will appear here:

```
dist/ww_controller_ui/ww_controller_ui.exe
```

### ⚠ IMPORTANT  
To use it properly:

👉 **Move the generated EXE to the ROOT of the project**, replacing the old one.

Example final structure:

```
windwaker-controller/
 ├─ ww_controller_ui.exe   ← Move it here
 ├─ python/
 ├─ assets/
 ├─ scripts/
 …
```

If the EXE stays inside `dist/`, it will NOT find your assets, scripts or Python runtime.

---

# 📄 License

This project is released under the **MIT License**.  
See the `LICENSE` file for details.

---

# 🤝 Contributions

Suggestions, bug reports, UI ideas and feature requests are always welcome!  
discord server : https://discord.com/invite/EDpVBx6P5e  
discord : .yewolf  
twitch : https://www.twitch.tv/yewolf  

