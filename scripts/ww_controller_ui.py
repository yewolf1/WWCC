import os
import subprocess
import sys
from tkinter import ttk, messagebox
import customtkinter as ctk

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

from scripts.ww_locale import tr, set_lang, get_lang

BG_MAIN = ("#F3F4F6", "#020617")
BG_CARD = ("#FFFFFF", "#0F172A")
FG_TEXT = ("#111827", "#E5E7EB")
FG_MUTED = ("#6B7280", "#9CA3AF")

ACCENT = ("#6366F1", "#6366F1")
ACCENT_HOVER = ("#4F46E5", "#4F46E5")

DANGER = ("#DC2626", "#EF4444")
DANGER_HOVER = ("#B91C1C", "#DC2626")

BTN_DEFAULT = ("#E5E7EB", "#1F2937")
BTN_DEFAULT_HOVER = ("#D1D5DB", "#4B5563")

TITLE_FONT = ("Segoe UI", 20, "bold")
SECTION_FONT = ("Segoe UI", 16, "bold")
NOTE_FONT = ("Segoe UI", 13, "italic")

CREATE_NO_WINDOW = 0

PY = r".\python\python.exe"
CMD = r".\scripts\ww_items_ntscu.py"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(relative):
    candidates = []
    if getattr(sys, "frozen", False):
        candidates.append(os.path.join(os.path.dirname(sys.executable), relative))
        if hasattr(sys, "_MEIPASS"):
            candidates.append(os.path.join(sys._MEIPASS, relative))
    candidates.append(os.path.join(BASE_DIR, relative))
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[-1]


ICON_ICO = resource_path("assets/ww_logo.ico")
if not os.path.exists(ICON_ICO):
    ICON_ICO = resource_path("assets/icon.ico")

ICON_IMG = resource_path("assets/ww_logo.png")
if not os.path.exists(ICON_IMG):
    ICON_IMG = resource_path("assets/ww_logo.ico")
if not os.path.exists(ICON_IMG):
    ICON_IMG = resource_path("assets/icon.png")
if not os.path.exists(ICON_IMG):
    ICON_IMG = resource_path("assets/icon.ico")
    
TWITCH_IMG = resource_path("assets/twitch_logo.png")
if not os.path.exists(TWITCH_IMG):
    TWITCH_IMG = resource_path("assets/twitch_logo.ico")

if hasattr(subprocess, "CREATE_NO_WINDOW"):
    CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW


def run_cmd(args, capture=False):
    full = [PY, CMD] + args
    try:
        if capture:
            result = subprocess.run(
                full,
                capture_output=True,
                text=True,
                creationflags=CREATE_NO_WINDOW,
            )
            if result.returncode != 0:
                msg = (result.stderr or "").strip() or tr("Erreur inconnue.")
                messagebox.showerror(tr("Erreur"), msg)
                return None
            return (result.stdout or "").strip()
        startup = None
        if hasattr(subprocess, "STARTUPINFO"):
            startup = subprocess.STARTUPINFO()
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(
            full,
            startupinfo=startup,
            creationflags=CREATE_NO_WINDOW,
        )
    except FileNotFoundError:
        messagebox.showerror(
            tr("Erreur"), tr("Impossible de trouver python portable ou ww_items_ntscu.py")
        )
    except Exception as e:
        messagebox.showerror(tr("Erreur"), str(e))


class App(ctk.CTk):
    def __init__(self):
        self.twitch_process = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # widgets traduisibles
        self._tr_widgets = []

        self.title(tr("Wind Waker Chaotic Controller"))
        try:
            self.iconbitmap(ICON_ICO)
        except Exception:
            pass

        self.logo_image = None
        if Image is not None:
            try:
                pil_img = Image.open(ICON_IMG)
                self.logo_image = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(28, 28),
                )
            except Exception:
                self.logo_image = None
                
        
        self.twitch_logo_image = None
        if Image is not None:
            try:
                if os.path.exists(TWITCH_IMG):
                    pil_twitch = Image.open(TWITCH_IMG)
                    self.twitch_logo_image = ctk.CTkImage(
                        light_image=pil_twitch,
                        dark_image=pil_twitch,
                        size=(20, 20),
                    )
            except Exception:
                self.twitch_logo_image = None

        self.geometry("1200x900")
        self.minsize(1000, 620)
        self.configure(fg_color=BG_MAIN)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.configure(width=230)

        self.content = ctk.CTkFrame(self, fg_color=BG_MAIN)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.sections = {}
        self.current_section = None
        self.nav_buttons = {}
        self.status_var = ctk.StringVar(value=tr("Prêt"))

        self.build_sidebar()
        self.build_sections()
        self.create_status_bar()
        self.show_section("items")

    def start_twitch_listener(self):
        # Empêche de lancer deux fois
        if self.twitch_process is not None and self.twitch_process.poll() is None:
            return

        twitch_main = resource_path(os.path.join("twitch_controller", "main.py"))

        if not os.path.exists(twitch_main):
            messagebox.showerror(tr("Twitch"), tr("Module Twitch introuvable."))
            return

        creationflags = 0
        if sys.platform.startswith("win") and hasattr(subprocess, "CREATE_NO_WINDOW"):
            creationflags = CREATE_NO_WINDOW

        try:
            # Utilise ton Python portable (PY)
            self.twitch_process = subprocess.Popen(
                [PY, twitch_main],
                creationflags=creationflags,
            )

            if hasattr(self, "twitch_status_label"):
                self.twitch_status_label.configure(
                    text=tr("Connecté à Twitch"),
                    text_color=("#16A34A", "#4ADE80"),
                )
            if hasattr(self, "twitch_button"):
                self.twitch_button.configure(state="disabled")
            if hasattr(self, "twitch_stop_button"):
                self.twitch_stop_button.configure(state="normal")

        except Exception as e:
            messagebox.showerror("Twitch", str(e))

    def stop_twitch_listener(self):
        try:
            if self.twitch_process is not None:
                # Process encore vivant ?
                if self.twitch_process.poll() is None:
                    self.twitch_process.terminate()
                self.twitch_process = None

            if hasattr(self, "twitch_status_label"):
                self.twitch_status_label.configure(
                    text=tr("Non connecté"),
                    text_color=FG_MUTED,
                )
            if hasattr(self, "twitch_button"):
                self.twitch_button.configure(state="normal")
            if hasattr(self, "twitch_stop_button"):
                self.twitch_stop_button.configure(state="disabled")

        except Exception as e:
            messagebox.showerror("Twitch", str(e))
            
    # ---- helpers pour gérer la traduction ----
    def _register_tr_widget(self, widget, key):
        widget._tr_key = key
        self._tr_widgets.append(widget)
        return widget

    def _tr_label(self, parent, key, **kwargs):
        return self._register_tr_widget(
            ctk.CTkLabel(parent, text=tr(key), **kwargs),
            key,
        )

    def _tr_button(self, parent, key, **kwargs):
        return self._register_tr_widget(
            ctk.CTkButton(parent, text=tr(key), **kwargs),
            key,
        )

    def _tr_checkbox(self, parent, key, **kwargs):
        return self._register_tr_widget(
            ctk.CTkCheckBox(parent, text=tr(key), **kwargs),
            key,
        )

    def _tr_radiobutton(self, parent, key, **kwargs):
        return self._register_tr_widget(
            ctk.CTkRadioButton(parent, text=tr(key), **kwargs),
            key,
        )

    def _tr_switch(self, parent, key, **kwargs):
        return self._register_tr_widget(
            ctk.CTkSwitch(parent, text=tr(key), **kwargs),
            key,
        )

    def refresh_labels(self):
        self.title(tr("Wind Waker Chaotic Controller"))
        for widget in self._tr_widgets:
            key = getattr(widget, "_tr_key", None)
            if key is not None:
                try:
                    widget.configure(text=tr(key))
                except Exception:
                    pass

    # ---- UI ----

    def build_sidebar(self):
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(18, 10))

        if self.logo_image is not None:
            icon_label = ctk.CTkLabel(header, image=self.logo_image, text=tr(""))
            icon_label.pack(side="left", padx=(0, 8))

        title = self._tr_label(
            header,
            "WW CC",
            text_color=FG_TEXT,
            font=TITLE_FONT,
        )
        title.pack(side="left")

        subtitle = self._tr_label(
            self.sidebar,
            "Contrôles temps réel pour\nWind Waker NTSC-U",
            text_color=FG_MUTED,
            font=("Segoe UI", 11),
            justify="left",
            anchor="w",
        )
        subtitle.pack(fill="x", padx=16, pady=(0, 16))

        theme_row = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        theme_row.pack(fill="x", padx=16, pady=(0, 8))
        theme_label = self._tr_label(
            theme_row,
            "Thème",
            text_color=FG_MUTED,
            font=("Segoe UI", 11),
        )
        theme_label.pack(side="left")

        self.theme_var = ctk.StringVar(value="Sombre")
        theme_switch = self._tr_switch(
            theme_row,
            "Clair / Sombre",
            variable=self.theme_var,
            onvalue="Sombre",
            offvalue="Clair",
            text_color=FG_TEXT,
            command=self.toggle_theme,
        )
        theme_switch.pack(side="right")

        # langue
        lang_row = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        lang_row.pack(fill="x", padx=16, pady=(0, 20))
        lang_label = self._tr_label(
            lang_row,
            "Langue",
            text_color=FG_MUTED,
            font=("Segoe UI", 11),
        )
        lang_label.pack(side="left")

        self.lang_var = ctk.StringVar(value="FR" if get_lang() == "fr" else "EN")
        lang_select = ctk.CTkSegmentedButton(
            lang_row,
            values=["FR", "EN"],
            variable=self.lang_var,
            command=self.on_lang_change,
        )
        lang_select.pack(side="right")

        buttons = [
            ("Items", "items"),
            ("Équipement", "equip"),
            ("Ressources", "resources"),
            ("Temps & météo", "time_weather"),
            ("Effets", "effects"),
            ("Système", "system"),
        ]
        for key, sec in buttons:
            btn = self._tr_button(
                self.sidebar,
                key,
                fg_color="transparent",
                hover_color=("#E5E7EB", "#111827"),
                text_color=FG_MUTED,
                anchor="w",
                corner_radius=8,
                height=36,
                command=lambda k=sec: self.show_section(k),
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[sec] = btn

        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(expand=True, fill="both")

        twitch_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color=("#F5F3FF", "#020617"),
            corner_radius=12,
            border_width=1,
            border_color=("#E5E7EB", "#111827"),
        )
        twitch_frame.pack(fill="x", padx=12, pady=(0, 10))

        header_row = ctk.CTkFrame(twitch_frame, fg_color="transparent")
        header_row.pack(fill="x", padx=10, pady=(8, 4))

        if self.twitch_logo_image is not None:
            logo = ctk.CTkLabel(header_row, image=self.twitch_logo_image, text="")
            logo.pack(side="left", padx=(0, 8))

        title_col = ctk.CTkFrame(header_row, fg_color="transparent")
        title_col.pack(side="left", fill="x", expand=True)

        twitch_title = self._tr_label(
            title_col,
            "Twitch",
            font=("Segoe UI", 14, "bold"),
            text_color=("#772CE8", "#C4B5FD"),
            anchor="w",
        )
        twitch_title.pack(anchor="w")

        self.twitch_status_label = self._tr_label(
            title_col,
            "Non connecté",
            font=("Segoe UI", 11),
            text_color=FG_MUTED,
            anchor="w",
        )
        self.twitch_status_label.pack(anchor="w")

        btn_row = ctk.CTkFrame(twitch_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(4, 10))

        self.twitch_button = self._tr_button(
            btn_row,
            "Connexion Twitch",
            command=self.start_twitch_listener,
            fg_color=("#9146FF", "#9146FF"),
            hover_color=("#772CE8", "#772CE8"),
            text_color="#FFFFFF",
            height=30,
            corner_radius=999,
        )
        self.twitch_button.pack(fill="x")

        self.twitch_stop_button = self._tr_button(
            btn_row,
            "Déconnexion Twitch",
            command=self.stop_twitch_listener,
            fg_color=DANGER,
            hover_color=DANGER_HOVER,
            text_color="#FFFFFF",
            height=28,
            corner_radius=999,
        )
        self.twitch_stop_button.pack(fill="x", pady=(6, 0))
        self.twitch_stop_button.configure(state="disabled")

        about_btn = self._tr_button(
            self.sidebar,
            "À propos",
            fg_color="transparent",
            hover_color=("#E5E7EB", "#111827"),
            text_color=FG_MUTED,
            anchor="w",
            corner_radius=8,
            height=32,
            command=self.show_about_window,
        )
        about_btn.pack(fill="x", padx=12, pady=(0, 14))

    def on_lang_change(self, value):
        lang_code = "fr" if value == "FR" else "en"
        set_lang(lang_code)
        self.refresh_labels()
        messagebox.showinfo(
            tr("Langue"),
            tr("Langue changée."),
        )

    def toggle_theme(self):
        mode = self.theme_var.get()
        if mode == "Clair":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
            
    def create_card(self, parent, title_key, description_key=None):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=14)
        card.pack(fill="x", padx=20, pady=12)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(10, 6))
        label = self._tr_label(
            header,
            title_key,
            text_color=FG_TEXT,
            font=SECTION_FONT,
        )
        label.pack(side="left")

        if description_key:
            desc = self._tr_label(
                card,
                description_key,
                text_color=FG_MUTED,
                font=("Segoe UI", 11),
                anchor="w",
                justify="left",
            )
            desc.pack(fill="x", padx=14, pady=(0, 8))

        line = ctk.CTkFrame(card, fg_color="#D1D5DB", height=1)
        line.pack(fill="x", padx=14, pady=(0, 8))
        return card

    def build_sections(self):
        keys = ["items", "equip", "resources", "time_weather", "effects", "system"]
        for key in keys:
            frame = ctk.CTkScrollableFrame(self.content, fg_color=BG_MAIN)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()
            self.sections[key] = frame

        self.build_items_section(self.sections["items"])
        self.build_equip_section(self.sections["equip"])
        self.build_resources_section(self.sections["resources"])
        self.build_time_weather_section(self.sections["time_weather"])
        self.build_effects_section(self.sections["effects"])
        self.build_system_section(self.sections["system"])

    def create_status_bar(self):
        bar = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        bar.grid_columnconfigure(0, weight=1)
        label = ctk.CTkLabel(
            bar,
            textvariable=self.status_var,
            text_color=FG_MUTED,
            anchor="w",
            font=("Segoe UI", 11),
        )
        label.grid(row=0, column=0, padx=14, pady=4)

    def set_status(self, text):
        self.status_var.set(text)

    def show_section(self, key):
        if self.current_section is not None:
            old = self.sections.get(self.current_section)
            if old is not None:
                old.grid_remove()
            old_btn = self.nav_buttons.get(self.current_section)
            if old_btn is not None:
                old_btn.configure(fg_color="transparent", text_color=FG_MUTED)
        frame = self.sections.get(key)
        if frame is not None:
            frame.grid()
        btn = self.nav_buttons.get(key)
        if btn is not None:
            btn.configure(fg_color=ACCENT, text_color="white")
        self.current_section = key

    def show_about_window(self):
        win = ctk.CTkToplevel(self)
        win.title(tr("À propos"))
        win.geometry("420x340")
        win.resizable(False, False)
        win.configure(fg_color=BG_CARD)

        try:
            win.iconbitmap(ICON_ICO)
        except Exception:
            pass

        frame = ctk.CTkFrame(win, fg_color=BG_CARD, corner_radius=16)
        frame.pack(fill="both", expand=True, padx=22, pady=22)

        if Image is not None and ImageTk is not None:
            try:
                img = Image.open(ICON_IMG).resize((72, 72))
                logo = ImageTk.PhotoImage(img)
                ttk.Label(frame, image=logo).pack(pady=(4, 8))
                win.logo_img = logo
            except Exception:
                pass

        title = self._tr_label(
            frame,
            "Wind Waker Chaotic Controller",
            text_color=FG_TEXT,
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(pady=(0, 4))

        version = self._tr_label(
            frame,
            "Version 1.0",
            text_color=FG_MUTED,
            font=("Segoe UI", 12),
        )
        version.pack()

        author = self._tr_label(
            frame,
            "Développé par Yewolf",
            text_color=FG_TEXT,
            font=("Segoe UI", 12),
        )
        author.pack(pady=(12, 0))

        link = self._tr_label(
            frame,
            "github.com/yewolf1/WWCC",
            text_color=FG_MUTED,
            font=("Segoe UI", 10, "italic"),
        )
        link.pack(pady=(4, 0))

        close_btn = self._tr_button(
            frame,
            "Fermer",
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="white",
            command=win.destroy,
        )
        close_btn.pack(pady=(22, 0))

        win.grab_set()

    # ---- sections ----

    def build_items_section(self, parent):
        card_items = self.create_card(
            parent, "Items", "Ajouter ou retirer rapidement les items principaux."
        )
        row = ctk.CTkFrame(card_items, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=6)

        label = self._tr_label(
            row,
            "Item",
            text_color=FG_TEXT,
            font=("Segoe UI", 12),
        )
        label.grid(row=0, column=0, sticky="w")

        items = [
            "telescope",
            "sail",
            "wind_waker",
            "grappling_hook",
            "spoils_bag",
            "boomerang",
            "deku_leaf",
            "tingle_tuner",
            "pictobox_dx",
            "iron_boots",
            "magic_armor",
            "bait_bag",
            "bow",
            "fire_ice_arrows",
            "light_arrows",
            "bombs",
            "delivery_bag",
            "hookshot",
            "skull_hammer",
        ]
        self.item_var = ctk.StringVar(value="boomerang")
        combo = ctk.CTkComboBox(
            row,
            variable=self.item_var,
            values=items,
            width=220,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        combo.grid(row=0, column=1, padx=8, pady=2, sticky="w")

        row.grid_columnconfigure(2, weight=1)

        actions = ctk.CTkFrame(card_items, fg_color="transparent")
        actions.pack(fill="x", padx=14, pady=(4, 10))

        btn_add = self._tr_button(
            actions,
            "Ajouter",
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="white",
            command=self.on_item_add,
        )
        btn_add.grid(row=0, column=0, padx=4, pady=4)

        btn_remove = self._tr_button(
            actions,
            "Retirer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_item_remove,
        )
        btn_remove.grid(row=0, column=1, padx=4, pady=4)

        timer_row = ctk.CTkFrame(card_items, fg_color="transparent")
        timer_row.pack(fill="x", padx=14, pady=(4, 10))
        label_timer = self._tr_label(
            timer_row,
            "Durée (s)",
            text_color=FG_TEXT,
        )
        label_timer.grid(row=0, column=0, sticky="w")
        self.item_timer_var = ctk.StringVar(value="10")
        entry_timer = ctk.CTkEntry(
            timer_row,
            textvariable=self.item_timer_var,
            width=70,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_timer.grid(row=0, column=1, padx=6)
        btn_timer = self._tr_button(
            timer_row,
            "Retirer pendant X sec",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_item_remove_timer,
        )
        btn_timer.grid(row=0, column=2, padx=6, pady=4)

        card_random = self.create_card(
            parent,
            "Item aléatoire",
            "Retire un item au hasard pendant un certain temps.",
        )
        rand_row = ctk.CTkFrame(card_random, fg_color="transparent")
        rand_row.pack(fill="x", padx=14, pady=6)
        label_rt = self._tr_label(
            rand_row,
            "Durée (s)",
            text_color=FG_TEXT,
        )
        label_rt.grid(row=0, column=0, sticky="w")
        self.random_timer_var = ctk.StringVar(value="10")
        entry_rt = ctk.CTkEntry(
            rand_row,
            textvariable=self.random_timer_var,
            width=70,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_rt.grid(row=0, column=1, padx=6)
        btn_random = self._tr_button(
            rand_row,
            "Retirer un item aléatoire",
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="white",
            command=self.on_item_random_timer,
        )
        btn_random.grid(row=0, column=2, padx=6, pady=4)

    def build_equip_section(self, parent):
        card_uneq = self.create_card(
            parent, "Déséquiper", "Vide un slot ou tous les slots X/Y/Z."
        )
        row = ctk.CTkFrame(card_uneq, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=6)

        self.unequip_slot_var = ctk.StringVar(value="x")
        rb_x = self._tr_radiobutton(
            row,
            "X",
            variable=self.unequip_slot_var,
            value="x",
            fg_color=ACCENT,
            text_color=FG_TEXT,
        )
        rb_y = self._tr_radiobutton(
            row,
            "Y",
            variable=self.unequip_slot_var,
            value="y",
            fg_color=ACCENT,
            text_color=FG_TEXT,
        )
        rb_z = self._tr_radiobutton(
            row,
            "Z",
            variable=self.unequip_slot_var,
            value="z",
            fg_color=ACCENT,
            text_color=FG_TEXT,
        )
        rb_x.grid(row=0, column=0, padx=4)
        rb_y.grid(row=0, column=1, padx=4)
        rb_z.grid(row=0, column=2, padx=4)

        self.unequip_all_var = ctk.BooleanVar(value=False)
        cb_all = self._tr_checkbox(
            row,
            "Tout déséquiper",
            variable=self.unequip_all_var,
            fg_color=ACCENT,
            text_color=FG_TEXT,
        )
        cb_all.grid(row=0, column=3, padx=14)

        btn_apply_uneq = self._tr_button(
            card_uneq,
            "Appliquer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_unequip,
        )
        btn_apply_uneq.pack(anchor="w", padx=14, pady=(4, 10))

        card_sword = self.create_card(
            parent, "Épée", "Change ou cycle la progression de l'épée."
        )
        sword_row = ctk.CTkFrame(card_sword, fg_color="transparent")
        sword_row.pack(fill="x", padx=14, pady=6)
        self.sword_stage_var = ctk.StringVar(value="hero")
        stages = [
            ("Off", "off"),
            ("Hero", "hero"),
            ("MS1", "ms1"),
            ("MS2", "ms2"),
            ("MS3", "ms3"),
        ]
        for i, (label_key, value) in enumerate(stages):
            rb = self._tr_radiobutton(
                sword_row,
                label_key,
                variable=self.sword_stage_var,
                value=value,
                fg_color=ACCENT,
                text_color=FG_TEXT,
            )
            rb.grid(row=0, column=i, padx=4)

        sword_btn_row = ctk.CTkFrame(card_sword, fg_color="transparent")
        sword_btn_row.pack(fill="x", padx=14, pady=(4, 10))
        btn_sword_set = self._tr_button(
            sword_btn_row,
            "Appliquer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_sword_set,
        )
        btn_sword_set.grid(row=0, column=0, padx=4)
        btn_sword_cycle = self._tr_button(
            sword_btn_row,
            "Cycle",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_sword_cycle,
        )
        btn_sword_cycle.grid(row=0, column=1, padx=4)

        card_shield = self.create_card(
            parent, "Bouclier", "Change ou cycle le bouclier actuel."
        )
        shield_row = ctk.CTkFrame(card_shield, fg_color="transparent")
        shield_row.pack(fill="x", padx=14, pady=6)
        self.shield_stage_var = ctk.StringVar(value="hero")
        shields = [
            ("Off", "off"),
            ("Hero", "hero"),
            ("Mirror", "mirror"),
        ]
        for i, (label_key, value) in enumerate(shields):
            rb = self._tr_radiobutton(
                shield_row,
                label_key,
                variable=self.shield_stage_var,
                value=value,
                fg_color=ACCENT,
                text_color=FG_TEXT,
            )
            rb.grid(row=0, column=i, padx=4)
        shield_btn_row = ctk.CTkFrame(card_shield, fg_color="transparent")
        shield_btn_row.pack(fill="x", padx=14, pady=(4, 10))
        btn_shield_set = self._tr_button(
            shield_btn_row,
            "Appliquer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_shield_set,
        )
        btn_shield_set.grid(row=0, column=0, padx=4)
        btn_shield_cycle = self._tr_button(
            shield_btn_row,
            "Cycle",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_shield_cycle,
        )
        btn_shield_cycle.grid(row=0, column=1, padx=4)

        card_tunic = self.create_card(
            parent,
            "Tunique",
            "Peut nécessiter un changement de zone pour s'afficher.",
        )
        tunic_row = ctk.CTkFrame(card_tunic, fg_color="transparent")
        tunic_row.pack(fill="x", padx=14, pady=6)
        self.tunic_stage_var = ctk.StringVar(value="green")
        tunics = [
            ("Verte", "green"),
            ("Bleue", "blue"),
        ]
        for i, (label_key, value) in enumerate(tunics):
            rb = self._tr_radiobutton(
                tunic_row,
                label_key,
                variable=self.tunic_stage_var,
                value=value,
                fg_color=ACCENT,
                text_color=FG_TEXT,
            )
            rb.grid(row=0, column=i, padx=4)
        tunic_btn_row = ctk.CTkFrame(card_tunic, fg_color="transparent")
        tunic_btn_row.pack(fill="x", padx=14, pady=(4, 10))
        btn_tunic_set = self._tr_button(
            tunic_btn_row,
            "Appliquer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_tunic_set,
        )
        btn_tunic_set.grid(row=0, column=0, padx=4)
        btn_tunic_cycle = self._tr_button(
            tunic_btn_row,
            "Cycle",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_tunic_cycle,
        )
        btn_tunic_cycle.grid(row=0, column=1, padx=4)

    def build_resources_section(self, parent):
        card_rupees = self.create_card(
            parent, "Rubis", "Lire ou modifier le nombre de rubis."
        )
        note_r = self._tr_label(
            card_rupees,
            "Peut nécessiter un changement de zone pour s'afficher.",
            text_color=FG_MUTED,
            font=NOTE_FONT,
            anchor="w",
            justify="left",
        )
        note_r.pack(anchor="w", padx=14, pady=(0, 6))

        row = ctk.CTkFrame(card_rupees, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=4)

        btn_get = self._tr_button(
            row,
            "Afficher",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_rupees_get,
        )
        btn_get.grid(row=0, column=0, padx=4, pady=4)

        label_set = self._tr_label(
            row,
            "Définir",
            text_color=FG_TEXT,
        )
        label_set.grid(row=0, column=1, padx=4)
        self.rupees_set_var = ctk.StringVar(value="0")
        entry_set = ctk.CTkEntry(
            row,
            textvariable=self.rupees_set_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_set.grid(row=0, column=2, padx=4)
        btn_set = self._tr_button(
            row,
            "Set",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_rupees_set,
        )
        btn_set.grid(row=0, column=3, padx=4)

        label_add = self._tr_label(
            row,
            "Ajouter",
            text_color=FG_TEXT,
        )
        label_add.grid(row=0, column=4, padx=4)
        self.rupees_add_var = ctk.StringVar(value="100")
        entry_add = ctk.CTkEntry(
            row,
            textvariable=self.rupees_add_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_add.grid(row=0, column=5, padx=4)
        btn_add = self._tr_button(
            row,
            "+",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            width=40,
            command=self.on_rupees_add,
        )
        btn_add.grid(row=0, column=6, padx=4)

        card_wallet = self.create_card(
            parent, "Portefeuille", "Change la capacité maximale de rubis."
        )
        wrow = ctk.CTkFrame(card_wallet, fg_color="transparent")
        wrow.pack(fill="x", padx=14, pady=6)
        label_tier = self._tr_label(
            wrow,
            "Tier",
            text_color=FG_TEXT,
        )
        label_tier.grid(row=0, column=0, padx=4)
        self.wallet_tier_var = ctk.StringVar(value="0")
        combo_tier = ctk.CTkComboBox(
            wrow,
            variable=self.wallet_tier_var,
            values=["0", "1", "2"],
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        combo_tier.grid(row=0, column=1, padx=4)
        btn_wallet_set = self._tr_button(
            wrow,
            "Set tier",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_wallet_set,
        )
        btn_wallet_set.grid(row=0, column=2, padx=4)
        btn_wallet_cycle = self._tr_button(
            wrow,
            "Cycle",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_wallet_cycle,
        )
        btn_wallet_cycle.grid(row=0, column=3, padx=4)

        card_magic = self.create_card(
            parent, "Magie", "Remplir, vider ou diviser la jauge de magie."
        )
        mrow = ctk.CTkFrame(card_magic, fg_color="transparent")
        mrow.pack(fill="x", padx=14, pady=6)
        btn_full = self._tr_button(
            mrow,
            "Full",
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="white",
            command=self.on_magic_full,
        )
        btn_half = self._tr_button(
            mrow,
            "Half",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_magic_half,
        )
        btn_empty = self._tr_button(
            mrow,
            "Empty",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_magic_empty,
        )
        btn_full.grid(row=0, column=0, padx=4)
        btn_half.grid(row=0, column=1, padx=4)
        btn_empty.grid(row=0, column=2, padx=4)

        card_bombs = self.create_card(
            parent, "Bombes", "Lire ou modifier le nombre de bombes."
        )
        note_b = self._tr_label(
            card_bombs,
            "Peut nécessiter un changement de zone pour s'afficher.",
            text_color=FG_MUTED,
            font=NOTE_FONT,
            anchor="w",
            justify="left",
        )
        note_b.pack(anchor="w", padx=14, pady=(0, 6))
        brow = ctk.CTkFrame(card_bombs, fg_color="transparent")
        brow.pack(fill="x", padx=14, pady=6)
        btn_empty_b = self._tr_button(
            brow,
            "Vider",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_bombs_empty,
        )
        btn_empty_b.grid(row=0, column=0, padx=4)
        label_add_b = self._tr_label(
            brow,
            "Ajouter",
            text_color=FG_TEXT,
        )
        label_add_b.grid(row=0, column=1, padx=4)
        self.bombs_add_var = ctk.StringVar(value="5")
        entry_add_b = ctk.CTkEntry(
            brow,
            textvariable=self.bombs_add_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_add_b.grid(row=0, column=2, padx=4)
        btn_add_b = self._tr_button(
            brow,
            "+",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            width=40,
            command=self.on_bombs_add,
        )
        btn_add_b.grid(row=0, column=3, padx=4)

        card_arrows = self.create_card(
            parent, "Flèches", "Lire ou modifier le nombre de flèches."
        )
        note_a = self._tr_label(
            card_arrows,
            "Peut nécessiter un changement de zone pour s'afficher.",
            text_color=FG_MUTED,
            font=NOTE_FONT,
            anchor="w",
            justify="left",
        )
        note_a.pack(anchor="w", padx=14, pady=(0, 6))
        arow = ctk.CTkFrame(card_arrows, fg_color="transparent")
        arow.pack(fill="x", padx=14, pady=6)
        btn_empty_a = self._tr_button(
            arow,
            "Vider",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_arrows_empty,
        )
        btn_empty_a.grid(row=0, column=0, padx=4)
        label_add_a = self._tr_label(
            arow,
            "Ajouter",
            text_color=FG_TEXT,
        )
        label_add_a.grid(row=0, column=1, padx=4)
        self.arrows_add_var = ctk.StringVar(value="10")
        entry_add_a = ctk.CTkEntry(
            arow,
            textvariable=self.arrows_add_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_add_a.grid(row=0, column=2, padx=4)
        btn_add_a = self._tr_button(
            arow,
            "+",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            width=40,
            command=self.on_arrows_add,
        )
        btn_add_a.grid(row=0, column=3, padx=4)

    def build_time_weather_section(self, parent):
        card_time = self.create_card(
            parent, "Temps", "Contrôle rapide de l'heure en jeu."
        )
        trow1 = ctk.CTkFrame(card_time, fg_color="transparent")
        trow1.pack(fill="x", padx=14, pady=4)
        btn_day = self._tr_button(
            trow1,
            "Jour",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_time_day,
        )
        btn_night = self._tr_button(
            trow1,
            "Nuit",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_time_night,
        )
        btn_dawn = self._tr_button(
            trow1,
            "Aube",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_time_dawn,
        )
        btn_dusk = self._tr_button(
            trow1,
            "Crépuscule",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_time_dusk,
        )
        btn_day.grid(row=0, column=0, padx=4, pady=2)
        btn_night.grid(row=0, column=1, padx=4, pady=2)
        btn_dawn.grid(row=0, column=2, padx=4, pady=2)
        btn_dusk.grid(row=0, column=3, padx=4, pady=2)

        trow2 = ctk.CTkFrame(card_time, fg_color="transparent")
        trow2.pack(fill="x", padx=14, pady=4)
        btn_cycle = self._tr_button(
            trow2,
            "Cycle",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_time_cycle,
        )
        btn_cycle.grid(row=0, column=0, padx=4)

        card_weather = self.create_card(
            parent, "Météo", "Forcer ou cycler la météo actuelle."
        )
        wrow1 = ctk.CTkFrame(card_weather, fg_color="transparent")
        wrow1.pack(fill="x", padx=14, pady=4)
        btn_clear = self._tr_button(
            wrow1,
            "Clear",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("clear"),
        )
        btn_cloudy = self._tr_button(
            wrow1,
            "Cloudy",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("cloudy"),
        )
        btn_rain = self._tr_button(
            wrow1,
            "Rain",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("rain"),
        )
        btn_storm = self._tr_button(
            wrow1,
            "Storm",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("storm"),
        )
        btn_clear.grid(row=0, column=0, padx=4, pady=2)
        btn_cloudy.grid(row=0, column=1, padx=4, pady=2)
        btn_rain.grid(row=0, column=2, padx=4, pady=2)
        btn_storm.grid(row=0, column=3, padx=4, pady=2)

        wrow2 = ctk.CTkFrame(card_weather, fg_color="transparent")
        wrow2.pack(fill="x", padx=14, pady=4)
        btn_fog = self._tr_button(
            wrow2,
            "Fog",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("fog"),
        )
        btn_tempest = self._tr_button(
            wrow2,
            "Tempest",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("tempest"),
        )
        btn_cycle_w = self._tr_button(
            wrow2,
            "Cycle",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=lambda: self.on_weather("cycle"),
        )
        btn_fog.grid(row=0, column=0, padx=4, pady=2)
        btn_tempest.grid(row=0, column=1, padx=4, pady=2)
        btn_cycle_w.grid(row=0, column=2, padx=4, pady=2)

    def build_effects_section(self, parent):
        card_freeze = self.create_card(
            parent, "Freeze mouvement", "Fige ou ralentit fortement les déplacements."
        )
        frow = ctk.CTkFrame(card_freeze, fg_color="transparent")
        frow.pack(fill="x", padx=14, pady=6)
        btn_on = self._tr_button(
            frow,
            "ON",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_freeze_on,
        )
        btn_off = self._tr_button(
            frow,
            "OFF",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_freeze_off,
        )
        btn_on.grid(row=0, column=0, padx=4)
        btn_off.grid(row=0, column=1, padx=4)
        label_timer = self._tr_label(
            frow,
            "Timer (s)",
            text_color=FG_TEXT,
        )
        label_timer.grid(row=0, column=2, padx=4)
        self.freeze_timer_var = ctk.StringVar(value="10")
        entry_freeze = ctk.CTkEntry(
            frow,
            textvariable=self.freeze_timer_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_freeze.grid(row=0, column=3, padx=4)
        btn_freeze_timer = self._tr_button(
            frow,
            "Freeze X sec",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_freeze_timer,
        )
        btn_freeze_timer.grid(row=0, column=4, padx=4)

        card_moon = self.create_card(
            parent, "Moonjump", "Augmente temporairement la hauteur de saut."
        )
        mrow1 = ctk.CTkFrame(card_moon, fg_color="transparent")
        mrow1.pack(fill="x", padx=14, pady=4)
        label_lvl = self._tr_label(
            mrow1,
            "Niveau",
            text_color=FG_TEXT,
        )
        label_lvl.grid(row=0, column=0, padx=4)
        self.moon_level_var = ctk.StringVar(value="1")
        combo_lvl = ctk.CTkComboBox(
            mrow1,
            variable=self.moon_level_var,
            values=["1", "2", "3"],
            width=70,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
            button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
        )
        combo_lvl.grid(row=0, column=1, padx=4)
        btn_moon_set = self._tr_button(
            mrow1,
            "Activer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_moon_set,
        )
        btn_moon_set.grid(row=0, column=2, padx=4)

        mrow2 = ctk.CTkFrame(card_moon, fg_color="transparent")
        mrow2.pack(fill="x", padx=14, pady=4)
        label_mt = self._tr_label(
            mrow2,
            "Timer (s)",
            text_color=FG_TEXT,
        )
        label_mt.grid(row=0, column=0, padx=4)
        self.moon_timer_var = ctk.StringVar(value="10")
        entry_mt = ctk.CTkEntry(
            mrow2,
            textvariable=self.moon_timer_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_mt.grid(row=0, column=1, padx=4)
        btn_moon_timer = self._tr_button(
            mrow2,
            "Activer X sec",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_moon_timer,
        )
        btn_moon_timer.grid(row=0, column=2, padx=4)
        btn_moon_off = self._tr_button(
            mrow2,
            "OFF",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_moon_off,
        )
        btn_moon_off.grid(row=0, column=3, padx=4)

        card_camera = self.create_card(
            parent, "Caméra", "Fixe la caméra ou lance un verrouillage temporaire."
        )
        crow = ctk.CTkFrame(card_camera, fg_color="transparent")
        crow.pack(fill="x", padx=14, pady=6)
        btn_cam_on = self._tr_button(
            crow,
            "Fixe ON",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_camera_on,
        )
        btn_cam_off = self._tr_button(
            crow,
            "Fixe OFF",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_camera_off,
        )
        btn_cam_on.grid(row=0, column=0, padx=4)
        btn_cam_off.grid(row=0, column=1, padx=4)
        label_ct = self._tr_label(
            crow,
            "Timer (s)",
            text_color=FG_TEXT,
        )
        label_ct.grid(row=0, column=2, padx=4)
        self.camera_timer_var = ctk.StringVar(value="10")
        entry_ct = ctk.CTkEntry(
            crow,
            textvariable=self.camera_timer_var,
            width=80,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        entry_ct.grid(row=0, column=3, padx=4)
        btn_cam_timer = self._tr_button(
            crow,
            "Fixe X sec",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_camera_timer,
        )
        btn_cam_timer.grid(row=0, column=4, padx=4)

    def build_system_section(self, parent):
        card_actions = self.create_card(
            parent, "Actions globales", "Contrôles rapides pour Link."
        )
        row = ctk.CTkFrame(card_actions, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=8)

        btn_kill = self._tr_button(
            row,
            "Kill Link",
            fg_color=DANGER,
            hover_color=DANGER_HOVER,
            text_color="white",
            command=self.on_kill,
        )
        btn_kill.grid(row=0, column=0, padx=4, pady=4)

        btn_hp_quarter = self._tr_button(
            row,
            "1/4 cœur",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_hp_quarter,
        )
        btn_hp_quarter.grid(row=0, column=1, padx=4, pady=4)

        btn_hp_three = self._tr_button(
            row,
            "3 cœurs",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_hp_three,
        )
        btn_hp_three.grid(row=0, column=2, padx=4, pady=4)

        hp_card = self.create_card(
            parent, "Santé avancée", "Ajuste précisément le nombre de cœurs."
        )
        hp_row = ctk.CTkFrame(hp_card, fg_color="transparent")
        hp_row.pack(fill="x", padx=14, pady=8)
        label_hp = self._tr_label(
            hp_row,
            "Cœurs",
            text_color=FG_TEXT,
        )
        label_hp.grid(row=0, column=0, padx=4)
        self.hp_value_var = ctk.DoubleVar(value=3.0)
        self.hp_display_var = ctk.StringVar(value="3.00")
        slider_hp = ctk.CTkSlider(
            hp_row,
            from_=0.25,
            to=20.0,
            number_of_steps=79,
            variable=self.hp_value_var,
            command=lambda v: self.hp_display_var.set(f"{float(v):.2f}"),
        )
        slider_hp.grid(row=0, column=1, padx=8, pady=4, sticky="ew")
        hp_row.grid_columnconfigure(1, weight=1)
        hp_display = ctk.CTkEntry(
            hp_row,
            textvariable=self.hp_display_var,
            width=70,
            fg_color=BG_MAIN,
            text_color=FG_TEXT,
        )
        hp_display.grid(row=0, column=2, padx=4)
        btn_hp_set = self._tr_button(
            hp_row,
            "Appliquer",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_hp_set,
        )
        btn_hp_set.grid(row=0, column=3, padx=4)

        card_list = self.create_card(
            parent, "Utilitaires", "Outils divers liés aux items."
        )
        lrow = ctk.CTkFrame(card_list, fg_color="transparent")
        lrow.pack(fill="x", padx=14, pady=8)
        btn_list = self._tr_button(
            lrow,
            "Lister les items",
            fg_color=BTN_DEFAULT,
            hover_color=BTN_DEFAULT_HOVER,
            text_color=FG_TEXT,
            command=self.on_list_items,
        )
        btn_list.grid(row=0, column=0, padx=4, pady=4)

    # ---- actions ----

    def on_item_add(self):
        item = self.item_var.get()
        run_cmd(["item", "--add", item])
        self.set_status(tr("Ajouté: {item}").format(item=item))

    def on_item_remove(self):
        item = self.item_var.get()
        run_cmd(["item", "--remove", item])
        self.set_status(tr("Retiré: {item}").format(item=item))

    def on_item_remove_timer(self):
        item = self.item_var.get()
        seconds = self.item_timer_var.get() or "10"
        run_cmd(["item", "--remove", item, "--timer", seconds])
        self.set_status(tr("Retiré {item} pendant {seconds}s").format(item=item, seconds=seconds))

    def on_item_random_timer(self):
        seconds = self.random_timer_var.get() or "10"
        out = run_cmd(["item", "--random", "--timer", seconds], capture=True)
        if out:
            self.set_status(out)

    def on_unequip(self):
        if self.unequip_all_var.get():
            run_cmd(["unequip", "--all"])
            self.set_status(tr("Slots X/Y/Z déséquipés"))
        else:
            slot = self.unequip_slot_var.get()
            run_cmd(["unequip", "--slot", slot])
            self.set_status(tr("Slot {slot} déséquipé").format(slot=slot.upper()))

    def on_sword_set(self):
        stage = self.sword_stage_var.get()
        run_cmd(["sword", "--stage", stage])
        self.set_status(tr("Épée: {stage}").format(stage=stage))

    def on_sword_cycle(self):
        run_cmd(["sword", "--cycle"])
        self.set_status(tr("Cycle épée"))

    def on_shield_set(self):
        stage = self.shield_stage_var.get()
        run_cmd(["shield", "--stage", stage])
        self.set_status(tr("Bouclier: {stage}").format(stage=stage))

    def on_shield_cycle(self):
        run_cmd(["shield", "--cycle"])
        self.set_status(tr("Cycle bouclier"))

    def on_tunic_set(self):
        stage = self.tunic_stage_var.get()
        run_cmd(["tunic", "--stage", stage])
        self.set_status(tr("Tunique: {stage}").format(stage=stage))

    def on_tunic_cycle(self):
        run_cmd(["tunic", "--cycle"])
        self.set_status(tr("Cycle tunique"))

    def on_rupees_get(self):
        out = run_cmd(["rupees", "--get"], capture=True)
        if out:
            self.set_status(out)

    def on_rupees_set(self):
        val = self.rupees_set_var.get() or "0"
        out = run_cmd(["rupees", "--set", val], capture=True)
        if out:
            self.set_status(out)

    def on_rupees_add(self):
        val = self.rupees_add_var.get() or "0"
        out = run_cmd(["rupees", "--add", val], capture=True)
        if out:
            self.set_status(out)

    def on_wallet_set(self):
        tier = self.wallet_tier_var.get()
        out = run_cmd(["wallet", "--tier", tier], capture=True)
        if out:
            self.set_status(out)

    def on_wallet_cycle(self):
        out = run_cmd(["wallet", "--cycle"], capture=True)
        if out:
            self.set_status(out)

    def on_magic_full(self):
        out = run_cmd(["magic", "--full"], capture=True)
        if out:
            self.set_status(out)

    def on_magic_half(self):
        out = run_cmd(["magic", "--half"], capture=True)
        if out:
            self.set_status(out)

    def on_magic_empty(self):
        out = run_cmd(["magic", "--empty"], capture=True)
        if out:
            self.set_status(out)

    def on_bombs_empty(self):
        out = run_cmd(["bombs", "--empty"], capture=True)
        if out:
            self.set_status(out)

    def on_bombs_add(self):
        val = self.bombs_add_var.get() or "0"
        out = run_cmd(["bombs", "--add", val], capture=True)
        if out:
            self.set_status(out)

    def on_arrows_empty(self):
        out = run_cmd(["arrows", "--empty"], capture=True)
        if out:
            self.set_status(out)

    def on_arrows_add(self):
        val = self.arrows_add_var.get() or "0"
        out = run_cmd(["arrows", "--add", val], capture=True)
        if out:
            self.set_status(out)

    def on_time_day(self):
        run_cmd(["time", "--day"])
        self.set_status(tr("Temps: jour"))

    def on_time_night(self):
        run_cmd(["time", "--night"])
        self.set_status(tr("Temps: nuit"))

    def on_time_dawn(self):
        run_cmd(["time", "--dawn"])
        self.set_status(tr("Temps: aube"))

    def on_time_dusk(self):
        run_cmd(["time", "--dusk"])
        self.set_status(tr("Temps: crépuscule"))

    def on_time_cycle(self):
        run_cmd(["time", "--cycle"])
        self.set_status(tr("Temps: cycle"))

    def on_weather(self, mode):
        if mode == "cycle":
            run_cmd(["weather", "--cycle"])
            self.set_status(tr("Météo: cycle"))
        else:
            run_cmd(["weather", f"--{mode}"])
            self.set_status(tr("Météo: {mode}").format(mode=mode))

    def on_freeze_on(self):
        run_cmd(["freeze", "--on"])
        self.set_status(tr("Freeze mouvement: ON"))

    def on_freeze_off(self):
        run_cmd(["freeze", "--off"])
        self.set_status(tr("Freeze mouvement: OFF"))

    def on_freeze_timer(self):
        val = self.freeze_timer_var.get() or "10"
        run_cmd(["freeze", "--timer", val])
        self.set_status(tr("Freeze pendant {seconds}s").format(seconds=val))

    def on_moon_set(self):
        lvl = self.moon_level_var.get()
        run_cmd(["moon", "--level", lvl])
        self.set_status(tr("Moonjump niveau {level}").format(level=lvl))

    def on_moon_timer(self):
        lvl = self.moon_level_var.get()
        sec = self.moon_timer_var.get() or "10"
        run_cmd(["moon", "--level", lvl, "--timer", sec])
        self.set_status(
            tr("Moonjump niveau {level} pendant {seconds}s").format(level=lvl, seconds=sec)
        )

    def on_moon_off(self):
        run_cmd(["moon", "--off"])
        self.set_status(tr("Moonjump OFF"))

    def on_camera_on(self):
        run_cmd(["camera", "--on"])
        self.set_status(tr("Caméra fixe ON"))

    def on_camera_off(self):
        run_cmd(["camera", "--off"])
        self.set_status(tr("Caméra fixe OFF"))

    def on_camera_timer(self):
        sec = self.camera_timer_var.get() or "10"
        run_cmd(["camera", "--timer", sec])
        self.set_status(tr("Caméra fixe pendant {seconds}s").format(seconds=sec))

    def on_kill(self):
        run_cmd(["kill"])
        self.set_status(tr("Kill Link"))

    def on_hp_quarter(self):
        run_cmd(["hp", "--quarter"])
        self.set_status(tr("Santé réglée à 1/4 de cœur"))

    def on_hp_three(self):
        run_cmd(["hp", "--three"])
        self.set_status(tr("Santé réglée à 3 cœurs"))

    def on_hp_set(self):
        try:
            hearts = float(self.hp_display_var.get())
        except ValueError:
            self.set_status(tr("Valeur de cœurs invalide"))
            return
        run_cmd(["hp", "--set", str(hearts)])
        self.set_status(tr("Santé réglée à {hearts} cœurs").format(hearts=hearts))

    def on_list_items(self):
        out = run_cmd(["list"], capture=True)
        if out:
            self.set_status(tr("Items disponibles"))
            win = ctk.CTkToplevel(self)
            win.title(tr("Liste des items"))
            win.geometry("320x420")
            win.configure(fg_color=BG_CARD)
            text = ctk.CTkTextbox(
                win,
                fg_color=BG_MAIN,
                text_color=FG_TEXT,
                corner_radius=10,
            )
            text.pack(fill="both", expand=True, padx=12, pady=12)
            text.insert("1.0", out)
            text.configure(state="disabled")
            win.grab_set()
            
    def on_close(self):
        try:
            self.stop_twitch_listener()
        except Exception:
            pass
        # Puis on ferme l'app
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
