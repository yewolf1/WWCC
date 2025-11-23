import json
import time
from pathlib import Path

import customtkinter as ctk

from ww_locale import tr

BASE_DIR = Path(__file__).resolve().parent
OVERLAY_STATE = BASE_DIR / "overlay_state.json"


class OverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WW Twitch Overlay")
        self.geometry("450x200+100+100")
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.9)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.configure(fg_color="#000000")

        self.container = ctk.CTkFrame(self, fg_color="#000000")
        self.container.pack(fill="both", expand=True, padx=8, pady=8)

        self.title_label = ctk.CTkLabel(
            self.container,
            text=tr("Aucun effet actif"),
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        )
        self.title_label.pack(anchor="w", pady=(0, 4))

        self.effects_frame = ctk.CTkFrame(self.container, fg_color="#0F172A")
        self.effects_frame.pack(fill="both", expand=True)

        self.effect_labels = []
        for _ in range(4):
            lbl = ctk.CTkLabel(
                self.effects_frame,
                text="",
                font=("Segoe UI", 16, "bold"),
                anchor="w",
                justify="left",
            )
            lbl.pack(fill="x", padx=8, pady=2)
            self.effect_labels.append(lbl)

        self._tick()

    # ------------------ DATA ------------------

    def _load_state(self):
        """Lit scripts/overlay_state.json et renvoie une liste d'effets actifs."""
        try:
            if not OVERLAY_STATE.exists():
                print("Overlay: fichier inexistant:", OVERLAY_STATE)
                return []

            raw = OVERLAY_STATE.read_text(encoding="utf-8")
            if not raw.strip():
                print("Overlay: fichier vide")
                return []

            data = json.loads(raw)
            if not isinstance(data, list):
                print("Overlay: JSON n'est pas une liste ->", type(data))
                return []

            now = time.time()
            active = []
            for e in data:
                try:
                    expires = float(e.get("expires_at", 0))
                except (TypeError, ValueError):
                    continue
                if expires > now:
                    active.append(e)

            active.sort(key=lambda e: e.get("expires_at", 0))
            print(f"Overlay: {len(active)} effet(s) actif(s)")
            return active
        except Exception as e:
            print("Overlay load error:", repr(e))
            return []

    def _format_effect_text(self, event, now):
        label = (event.get("label") or "").strip()
        user_input = (event.get("user_input") or "").strip()
        viewer = (event.get("viewer") or "").strip()
        duration = int(event.get("duration", 0))
        expires_at = event.get("expires_at", now)
        remaining = max(0, int(round(expires_at - now)))

        # 1ère ligne : "<viewer>: <label> (Xs)" ou juste "<label> (Xs)"
        base = label or tr("Effet inconnu")
        # si le nom de la reward contient déjà une durée entre parenthèses
        if duration > 0 and "(" not in base:
            base += f" ({remaining}s)"

        if viewer:
            line1 = f"{viewer}: {base}"
        else:
            line1 = base

        # 2e ligne : le message saisi (si utile)
        # on ignore les trucs du style "Undefined"
        if user_input and user_input.lower() != "undefined":
            return f"{line1}\n{user_input}"

        return line1

    # ------------------ RENDER ------------------

    def _tick(self):
        now = time.time()
        events = self._load_state()

        for i, lbl in enumerate(self.effect_labels):
            if i < len(events):
                text = self._format_effect_text(events[i], now)
                lbl.configure(text=text)
            else:
                lbl.configure(text="")

        if events:
            self.title_label.configure(text=tr("Effets actifs"))
        else:
            self.title_label.configure(text=tr("Aucun effet actif"))

        self.after(200, self._tick)


if __name__ == "__main__":
    app = OverlayApp()
    app.mainloop()
