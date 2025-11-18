import psutil

print("=== PROCESSUS DETECTES ===")
found = False
for proc in psutil.process_iter(['pid', 'name']):
    try:
        name = proc.info['name']
        if 'dolphin' in name.lower():
            print(f"✔ {name} (PID {proc.pid})")
            found = True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

if not found:
    print("❌ Aucun processus Dolphin détecté. Essaie de lancer Dolphin avant.")
