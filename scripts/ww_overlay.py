import json
import os
import time
from pathlib import Path

import customtkinter as ctk

from ww_locale import tr

BASE_DIR = Path(__file__).resolve().parent
OVERLAY_STATE = BASE_DIR / "overlay_state.json"

# Couleurs Light / Dark (comme ton UI principale)
BG_MAIN = ("#F3F4F6", "#020617")
BG_CARD = ("#FFFFFF", "#0F172A")
FG_TEXT = ("#111827", "#E5E7EB")
VIEWER_COLOR = ("#7C3AED", "#C4B5FD")  # pseudo façon Twitch


class OverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WW Twitch Overlay")

        # Taille & position
        self.geometry("280x450+100+100")
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.9)

        # Thème reçu de l'appli principale (WW_THEME = "light" / "dark")
        theme = os.getenv("WW_THEME", "dark").lower()
        if theme in ("light", "clair"):
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Fond global
        self.configure(fg_color=BG_MAIN)

        self.container = ctk.CTkFrame(self, fg_color=BG_MAIN)
        self.container.pack(fill="both", expand=True, padx=8, pady=8)

        self.title_label = ctk.CTkLabel(
            self.container,
            text=tr("Effets actifs"),
            font=("Segoe UI", 18, "bold"),
            text_color=FG_TEXT,
        )
        self.title_label.pack(anchor="w", pady=(0, 4))

        # Zone qui contient les "cartes" d'effets
        self.effects_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.effects_frame.pack(fill="both", expand=True, padx=2, pady=2)

        self.rows = []
        self._build_effect_rows(5)  # max 5 logs affichés

        self._tick()

    def _build_effect_rows(self, count: int):
        for child in self.effects_frame.winfo_children():
            child.destroy()
        self.rows.clear()

        for _ in range(count):
            # Carte pour UN log
            card = ctk.CTkFrame(
                self.effects_frame,
                fg_color=BG_CARD,
                corner_radius=12,
            )

            user_lbl = ctk.CTkLabel(
                card,
                text="",
                font=("Segoe UI", 13, "bold"),
                text_color=VIEWER_COLOR,
                anchor="w",
                justify="left",
            )
            user_lbl.pack(fill="x", anchor="w", padx=10, pady=(6, 0))

            msg_lbl = ctk.CTkLabel(
                card,
                text="",
                font=("Segoe UI", 14),
                text_color=FG_TEXT,
                anchor="w",
                justify="left",
            )
            msg_lbl.pack(fill="x", anchor="w", padx=10, pady=(2, 6))

            self.rows.append(
                {
                    "frame": card,
                    "user": user_lbl,
                    "msg": msg_lbl,
                }
            )

    def _load_state(self):
        if not OVERLAY_STATE.exists():
            return []

        try:
            raw = OVERLAY_STATE.read_text(encoding="utf-8")
            if not raw.strip():
                return []
            data = json.loads(raw)
        except Exception:
            return []

        now = time.time()
        # Garder uniquement les effets dont le timer n'est pas fini
        active = [e for e in data if e.get("expires_at", 0) > now]

        # Style chat : derniers reçus en premier
        active.sort(key=lambda e: e.get("created_at", 0), reverse=True)
        return active

    def _format_effect_parts(self, event, now):
        raw_label = (event.get("label") or "").strip()
        user_input = (event.get("user_input") or "").strip()
        viewer = (event.get("viewer") or "").strip()

        duration = int(event.get("duration", 0))
        expires_at = event.get("expires_at", now)
        remaining = max(0, int(round(expires_at - now)))

        label = tr(raw_label) if raw_label else ""
        effect_text = label or raw_label

        if duration > 0 and effect_text:
            if "(" not in effect_text:
                effect_text += f" ({remaining}s)"
            else:
                effect_text += f" ({remaining}s)"

        message_lines = []
        if effect_text:
            message_lines.append(effect_text)

        if user_input and user_input.lower() != "undefined":
            message_lines.append(user_input)

        message_text = "\n".join(message_lines)
        username_text = viewer

        if not username_text and not message_text:
            message_text = tr("Effet inconnu")

        return username_text, message_text

    def _tick(self):
        now = time.time()
        events = self._load_state()
        nb = min(len(events), len(self.rows))

        if nb == 0:
            self.title_label.configure(text=tr("Aucun effet actif"))
        else:
            self.title_label.configure(text=f"{tr('Effets actifs')} ({nb})")

        for idx, row in enumerate(self.rows):
            frame = row["frame"]
            user_lbl = row["user"]
            msg_lbl = row["msg"]

            if idx < nb:
                username, message = self._format_effect_parts(events[idx], now)
                if not frame.winfo_manager():
                    frame.pack(fill="x", padx=4, pady=4)
                user_lbl.configure(text=username)
                msg_lbl.configure(text=message)
            else:
                if frame.winfo_manager():
                    frame.pack_forget()
                user_lbl.configure(text="")
                msg_lbl.configure(text="")

        self.after(200, self._tick)


if __name__ == "__main__":
    app = OverlayApp()
    app.mainloop()
