import os

_LANG = os.getenv("WW_LANG", "fr").lower()
if _LANG not in ("fr", "en"):
    _LANG = "fr"

_STRINGS = {
    "": {"fr": "", "en": ""},
    "+": {"fr": "+", "en": "+"},

    "Erreur": {"fr": "Erreur", "en": "Error"},
    "Erreur inconnue.": {"fr": "Erreur inconnue.", "en": "Unknown error."},
    "Impossible de trouver python portable ou ww_items_ntscu.py": {
        "fr": "Impossible de trouver python portable ou ww_items_ntscu.py",
        "en": "Could not find portable Python or ww_items_ntscu.py",
    },

    "WW Controller": {"fr": "WW Controller", "en": "WW Controller"},
    "Wind Waker Chaotic Controller": {
        "fr": "Wind Waker Chaotic Controller",
        "en": "Wind Waker Chaotic Controller",
    },
    "Contrôles temps réel pour\nWind Waker NTSC-U": {
        "fr": "Contrôles temps réel pour\nWind Waker NTSC-U",
        "en": "Realtime controls for\nWind Waker NTSC-U",
    },

    "Thème": {"fr": "Thème", "en": "Theme"},
    "Clair / Sombre": {"fr": "Clair / Sombre", "en": "Light / Dark"},
    "Items": {"fr": "Items", "en": "Items"},
    "Équipement": {"fr": "Équipement", "en": "Equipment"},
    "Ressources": {"fr": "Ressources", "en": "Resources"},
    "Temps & météo": {"fr": "Temps & météo", "en": "Time & weather"},
    "Effets": {"fr": "Effets", "en": "Effects"},
    "Système": {"fr": "Système", "en": "System"},
    "À propos": {"fr": "À propos", "en": "About"},

    "Version 1.0": {"fr": "Version 1.0", "en": "Version 1.0"},
    "Développé par Yewolf": {"fr": "Développé par Yewolf", "en": "Developed by Yewolf"},
    "github.com/yewolf/windwaker-controller": {
        "fr": "github.com/yewolf/windwaker-controller",
        "en": "github.com/yewolf/windwaker-controller",
    },
    "Fermer": {"fr": "Fermer", "en": "Close"},

    "Ajouter ou retirer rapidement les items principaux.": {
        "fr": "Ajouter ou retirer rapidement les items principaux.",
        "en": "Quickly add or remove main items.",
    },
    "Item": {"fr": "Item", "en": "Item"},
    "Ajouter": {"fr": "Ajouter", "en": "Add"},
    "Retirer": {"fr": "Retirer", "en": "Remove"},
    "Durée (s)": {"fr": "Durée (s)", "en": "Duration (s)"},
    "Retirer pendant X sec": {
        "fr": "Retirer pendant X sec",
        "en": "Remove for X sec",
    },
    "Item aléatoire": {"fr": "Item aléatoire", "en": "Random item"},
    "Retire un item au hasard pendant un certain temps.": {
        "fr": "Retire un item au hasard pendant un certain temps.",
        "en": "Removes a random item for some time.",
    },
    "Retirer un item aléatoire": {
        "fr": "Retirer un item aléatoire",
        "en": "Remove a random item",
    },

    "Déséquiper": {"fr": "Déséquiper", "en": "Unequip"},
    "Vide un slot ou tous les slots X/Y/Z.": {
        "fr": "Vide un slot ou tous les slots X/Y/Z.",
        "en": "Empty one slot or all slots X/Y/Z.",
    },
    "X": {"fr": "X", "en": "X"},
    "Y": {"fr": "Y", "en": "Y"},
    "Z": {"fr": "Z", "en": "Z"},
    "Tout déséquiper": {"fr": "Tout déséquiper", "en": "Unequip all"},
    "Appliquer": {"fr": "Appliquer", "en": "Apply"},

    "Épée": {"fr": "Épée", "en": "Sword"},
    "Change ou cycle la progression de l'épée.": {
        "fr": "Change ou cycle la progression de l'épée.",
        "en": "Change or cycle the sword progression.",
    },
    "Off": {"fr": "Off", "en": "Off"},
    "Hero": {"fr": "Hero", "en": "Hero"},
    "MS1": {"fr": "MS1", "en": "MS1"},
    "MS2": {"fr": "MS2", "en": "MS2"},
    "MS3": {"fr": "MS3", "en": "MS3"},

    "Bouclier": {"fr": "Bouclier", "en": "Shield"},
    "Change ou cycle le bouclier actuel.": {
        "fr": "Change ou cycle le bouclier actuel.",
        "en": "Change or cycle the current shield.",
    },
    "Mirror": {"fr": "Mirror", "en": "Mirror"},

    "Tunique": {"fr": "Tunique", "en": "Tunic"},
    "Peut nécessiter un changement de zone pour s'afficher.": {
        "fr": "Peut nécessiter un changement de zone pour s'afficher.",
        "en": "May require changing area to refresh display.",
    },
    "Verte": {"fr": "Verte", "en": "Green"},
    "Bleue": {"fr": "Bleue", "en": "Blue"},

    "Rubis": {"fr": "Rubis", "en": "Rupees"},
    "Lire ou modifier le nombre de rubis.": {
        "fr": "Lire ou modifier le nombre de rubis.",
        "en": "Read or edit the number of rupees.",
    },
    "Afficher": {"fr": "Afficher", "en": "Show"},
    "Définir": {"fr": "Définir", "en": "Set"},
    "Set": {"fr": "Set", "en": "Set"},

    "Portefeuille": {"fr": "Portefeuille", "en": "Wallet"},
    "Change la capacité maximale de rubis.": {
        "fr": "Change la capacité maximale de rubis.",
        "en": "Change the maximum rupee capacity.",
    },
    "Tier": {"fr": "Tier", "en": "Tier"},
    "Set tier": {"fr": "Set tier", "en": "Set tier"},
    "Cycle": {"fr": "Cycle", "en": "Cycle"},

    "Magie": {"fr": "Magie", "en": "Magic"},
    "Remplir, vider ou diviser la jauge de magie.": {
        "fr": "Remplir, vider ou diviser la jauge de magie.",
        "en": "Fill, empty or halve the magic meter.",
    },
    "Full": {"fr": "Full", "en": "Full"},
    "Half": {"fr": "Half", "en": "Half"},
    "Empty": {"fr": "Empty", "en": "Empty"},

    "Bombes": {"fr": "Bombes", "en": "Bombs"},
    "Lire ou modifier le nombre de bombes.": {
        "fr": "Lire ou modifier le nombre de bombes.",
        "en": "Read or edit the number of bombs.",
    },
    "Vider": {"fr": "Vider", "en": "Empty"},

    "Flèches": {"fr": "Flèches", "en": "Arrows"},
    "Lire ou modifier le nombre de flèches.": {
        "fr": "Lire ou modifier le nombre de flèches.",
        "en": "Read or edit the number of arrows.",
    },

    "Temps": {"fr": "Temps", "en": "Time"},
    "Contrôle rapide de l'heure en jeu.": {
        "fr": "Contrôle rapide de l'heure en jeu.",
        "en": "Quick control of in-game time.",
    },
    "Jour": {"fr": "Jour", "en": "Day"},
    "Nuit": {"fr": "Nuit", "en": "Night"},
    "Aube": {"fr": "Aube", "en": "Dawn"},
    "Crépuscule": {"fr": "Crépuscule", "en": "Dusk"},
    "Set (°)": {"fr": "Set (°)", "en": "Set (°)"},

    "Météo": {"fr": "Météo", "en": "Weather"},
    "Forcer ou cycler la météo actuelle.": {
        "fr": "Forcer ou cycler la météo actuelle.",
        "en": "Force or cycle the current weather.",
    },
    "Clear": {"fr": "Clear", "en": "Clear"},
    "Cloudy": {"fr": "Cloudy", "en": "Cloudy"},
    "Rain": {"fr": "Rain", "en": "Rain"},
    "Storm": {"fr": "Storm", "en": "Storm"},
    "Fog": {"fr": "Fog", "en": "Fog"},
    "Tempest": {"fr": "Tempest", "en": "Tempest"},

    "Freeze mouvement": {"fr": "Freeze mouvement", "en": "Freeze movement"},
    "Fige ou ralentit fortement les déplacements.": {
        "fr": "Fige ou ralentit fortement les déplacements.",
        "en": "Freeze or heavily slow movement.",
    },
    "ON": {"fr": "ON", "en": "ON"},
    "OFF": {"fr": "OFF", "en": "OFF"},
    "Timer (s)": {"fr": "Timer (s)", "en": "Timer (s)"},
    "Freeze X sec": {"fr": "Freeze X sec", "en": "Freeze X sec"},

    "Moonjump": {"fr": "Moonjump", "en": "Moonjump"},
    "Augmente temporairement la hauteur de saut.": {
        "fr": "Augmente temporairement la hauteur de saut.",
        "en": "Temporarily increases jump height.",
    },
    "Niveau": {"fr": "Niveau", "en": "Level"},
    "Activer": {"fr": "Activer", "en": "Activate"},
    "Activer X sec": {"fr": "Activer X sec", "en": "Activate X sec"},

    "Caméra": {"fr": "Caméra", "en": "Camera"},
    "Fixe la caméra ou lance un verrouillage temporaire.": {
        "fr": "Fixe la caméra ou lance un verrouillage temporaire.",
        "en": "Lock the camera or start a temporary lock.",
    },
    "Fixe ON": {"fr": "Fixe ON", "en": "Lock ON"},
    "Fixe OFF": {"fr": "Fixe OFF", "en": "Lock OFF"},
    "Fixe X sec": {"fr": "Fixe X sec", "en": "Lock X sec"},

    "Actions globales": {"fr": "Actions globales", "en": "Global actions"},
    "Contrôles rapides pour Link.": {
        "fr": "Contrôles rapides pour Link.",
        "en": "Quick controls for Link.",
    },
    "Kill Link": {"fr": "Kill Link", "en": "Kill Link"},
    "1/4 cœur": {"fr": "1/4 cœur", "en": "1/4 heart"},
    "3 cœurs": {"fr": "3 cœurs", "en": "3 hearts"},

    "Santé avancée": {"fr": "Santé avancée", "en": "Advanced health"},
    "Ajuste précisément le nombre de cœurs.": {
        "fr": "Ajuste précisément le nombre de cœurs.",
        "en": "Precisely adjust the number of hearts.",
    },
    "Cœurs": {"fr": "Cœurs", "en": "Hearts"},

    "Utilitaires": {"fr": "Utilitaires", "en": "Tools"},
    "Outils divers liés aux items.": {
        "fr": "Outils divers liés aux items.",
        "en": "Various item-related tools.",
    },
    "Lister les items": {"fr": "Lister les items", "en": "List items"},
    "Liste des items": {"fr": "Liste des items", "en": "Items list"},

    "Langue": {"fr": "Langue", "en": "Language"},
    "La langue sera appliquée aux nouveaux textes. Redémarre l'application pour tout traduire.": {
    "fr": "La langue sera appliquée aux nouveaux textes. Redémarre l'application pour tout traduire.",
    "en": "Language will be applied to new texts. Restart the application to translate everything.",
    },
    
    "Langue changée.": {
        "fr": "Langue changée.",
        "en": "Language changed.",
    },

    "Prêt": {"fr": "Prêt", "en": "Ready"},
    "Ajouté: {item}": {"fr": "Ajouté: {item}", "en": "Added: {item}"},
    "Retiré: {item}": {"fr": "Retiré: {item}", "en": "Removed: {item}"},
    "Retiré {item} pendant {seconds}s": {
        "fr": "Retiré {item} pendant {seconds}s",
        "en": "Removed {item} for {seconds}s",
    },
    "Slots X/Y/Z déséquipés": {
        "fr": "Slots X/Y/Z déséquipés",
        "en": "Slots X/Y/Z unequipped",
    },
    "Slot {slot} déséquipé": {
        "fr": "Slot {slot} déséquipé",
        "en": "Slot {slot} unequipped",
    },
    "Épée: {stage}": {"fr": "Épée: {stage}", "en": "Sword: {stage}"},
    "Cycle épée": {"fr": "Cycle épée", "en": "Sword cycle"},
    "Bouclier: {stage}": {"fr": "Bouclier: {stage}", "en": "Shield: {stage}"},
    "Cycle bouclier": {"fr": "Cycle bouclier", "en": "Shield cycle"},
    "Tunique: {stage}": {"fr": "Tunique: {stage}", "en": "Tunic: {stage}"},
    "Cycle tunique": {"fr": "Cycle tunique", "en": "Tunic cycle"},

    "Temps: jour": {"fr": "Temps: jour", "en": "Time: day"},
    "Temps: nuit": {"fr": "Temps: nuit", "en": "Time: night"},
    "Temps: aube": {"fr": "Temps: aube", "en": "Time: dawn"},
    "Temps: crépuscule": {"fr": "Temps: crépuscule", "en": "Time: dusk"},
    "Temps: cycle": {"fr": "Temps: cycle", "en": "Time: cycle"},

    "Météo: cycle": {"fr": "Météo: cycle", "en": "Weather: cycle"},
    "Météo: {mode}": {"fr": "Météo: {mode}", "en": "Weather: {mode}"},

    "Freeze mouvement: ON": {
        "fr": "Freeze mouvement: ON",
        "en": "Freeze movement: ON",
    },
    "Freeze mouvement: OFF": {
        "fr": "Freeze mouvement: OFF",
        "en": "Freeze movement: OFF",
    },
    "Freeze pendant {seconds}s": {
        "fr": "Freeze pendant {seconds}s",
        "en": "Freeze for {seconds}s",
    },

    "Moonjump niveau {level}": {
        "fr": "Moonjump niveau {level}",
        "en": "Moonjump level {level}",
    },
    "Moonjump niveau {level} pendant {seconds}s": {
        "fr": "Moonjump niveau {level} pendant {seconds}s",
        "en": "Moonjump level {level} for {seconds}s",
    },
    "Moonjump OFF": {"fr": "Moonjump OFF", "en": "Moonjump OFF"},

    "Caméra fixe ON": {"fr": "Caméra fixe ON", "en": "Camera lock ON"},
    "Caméra fixe OFF": {"fr": "Caméra fixe OFF", "en": "Camera lock OFF"},
    "Caméra fixe pendant {seconds}s": {
        "fr": "Caméra fixe pendant {seconds}s",
        "en": "Camera lock for {seconds}s",
    },

    "Santé réglée à 1/4 de cœur": {
        "fr": "Santé réglée à 1/4 de cœur",
        "en": "Health set to 1/4 heart",
    },
    "Santé réglée à 3 cœurs": {
        "fr": "Santé réglée à 3 cœurs",
        "en": "Health set to 3 hearts",
    },
    "Santé réglée à {hearts} cœurs": {
        "fr": "Santé réglée à {hearts} cœurs",
        "en": "Health set to {hearts} hearts",
    },
    "Valeur de cœurs invalide": {
        "fr": "Valeur de cœurs invalide",
        "en": "Invalid hearts value",
    },

    "Items disponibles": {
        "fr": "Items disponibles",
        "en": "Items available",
    },
    "Twitch": {"fr": "Twitch", "en": "Twitch"},
    "Non connecté": {"fr": "Non connecté", "en": "Not connected"},
    "Connecté à Twitch": {
        "fr": "Connecté à Twitch",
        "en": "Connected to Twitch",
    },
    "Connexion Twitch": {
        "fr": "Connexion Twitch",
        "en": "Connect to Twitch",
    },
    "Module Twitch introuvable.": {
        "fr": "Module Twitch introuvable.",
        "en": "Twitch module not found.",
    },
    "Déconnexion Twitch": {
        "fr": "Déconnexion Twitch",
        "en": "Disconnect Twitch",
    },
    
    "Vagues": {"fr": "Vagues", "en": "Waves"},
    "Contrôle l'agitation de la mer.": {
        "fr": "Contrôle l'agitation de la mer.",
        "en": "Control of the waves in the sea.",
    },
    
    "off": {"fr": "off", "en": "off"},
    "medium": {"fr": "Moyen", "en": "Medium"},
    "big": {"fr": "Grosses Vagues", "en": "Big"},
    "freak": {"fr": "Incontrôlables", "en": "Freak"},
    "apocalyptic": {"fr": "Apocaliptiques", "en": "Apocalyptic"},
    
    "Effets actifs": {"fr": "Effets actifs", "en": "Active effects"},
    "Aucun effet actif": {"fr": "Aucun effet actif", "en": "No active effect"},
    "Overlay Twitch": {
        "fr": "Overlay Twitch",
        "en": "Twitch overlay",
    },
    "Effets actifs": {
        "fr": "Effets actifs",
        "en": "Active effects",
    },
    "Aucun effet actif": {
        "fr": "Aucun effet actif",
        "en": "No active effect",
    },
     # Récompenses Twitch (twitch_config.json)
    "Kill Link": {
        "fr": "Tuer Link",
        "en": "Kill Link",
    },
    "1/4 heart": {
        "fr": "1/4 de cœur",
        "en": "1/4 heart",
    },
    "3 hearts": {
        "fr": "3 cœurs",
        "en": "3 hearts",
    },
    "Set HP to 10 hearts": {
        "fr": "Vie à 10 cœurs",
        "en": "Set HP to 10 hearts",
    },

    "Unequip slot X": {
        "fr": "Déséquiper slot X",
        "en": "Unequip slot X",
    },
    "Unequip slot Y": {
        "fr": "Déséquiper slot Y",
        "en": "Unequip slot Y",
    },
    "Unequip slot Z": {
        "fr": "Déséquiper slot Z",
        "en": "Unequip slot Z",
    },
    "Unequip all slots": {
        "fr": "Déséquiper tous les slots",
        "en": "Unequip all slots",
    },

    "Sword (viewer choice)": {
        "fr": "Épée (choix du viewer)",
        "en": "Sword (viewer choice)",
    },
    "Shield (viewer choice)": {
        "fr": "Bouclier (choix du viewer)",
        "en": "Shield (viewer choice)",
    },
    "Tunic (viewer choice)": {
        "fr": "Tunique (choix du viewer)",
        "en": "Tunic (viewer choice)",
    },

    "Rupees +50": {
        "fr": "Rubis +50",
        "en": "Rupees +50",
    },
    "Rupees -50": {
        "fr": "Rubis -50",
        "en": "Rupees -50",
    },
    "Rupees set to 0": {
        "fr": "Rubis mis à 0",
        "en": "Rupees set to 0",
    },
    "Rupees max wallet": {
        "fr": "Rubis : portefeuille max",
        "en": "Rupees max wallet",
    },

    "Wallet: Tier 0": {
        "fr": "Portefeuille : palier 0",
        "en": "Wallet: Tier 0",
    },
    "Wallet: Tier 1": {
        "fr": "Portefeuille : palier 1",
        "en": "Wallet: Tier 1",
    },
    "Wallet: Tier 2": {
        "fr": "Portefeuille : palier 2",
        "en": "Wallet: Tier 2",
    },
    "Wallet: Cycle": {
        "fr": "Portefeuille : cycle",
        "en": "Wallet: Cycle",
    },

    "Time (viewer choice)": {
        "fr": "Heure (choix du viewer)",
        "en": "Time (viewer choice)",
    },
    "Weather (viewer choice)": {
        "fr": "Météo (choix du viewer)",
        "en": "Weather (viewer choice)",
    },

    "Freeze ON": {
        "fr": "Freeze ON",
        "en": "Freeze ON",
    },
    "Freeze OFF": {
        "fr": "Freeze OFF",
        "en": "Freeze OFF",
    },
    "Freeze 10s": {
        "fr": "Freeze 10 s",
        "en": "Freeze 10s",
    },
    "Freeze 30s": {
        "fr": "Freeze 30 s",
        "en": "Freeze 30s",
    },

    "Moonjump x1 (10s)": {
        "fr": "Moonjump x1 (10s)",
        "en": "Moonjump x1 (10s)",
    },
    "Moonjump x2 (30s)": {
        "fr": "Moonjump x2 (30s)",
        "en": "Moonjump x2 (30s)",
    },
    "Moonjump x3 (30s)": {
        "fr": "Moonjump x3 (30s)",
        "en": "Moonjump x3 (30s)",
    },
    "Moonjump OFF": {
        "fr": "Moonjump OFF",
        "en": "Moonjump OFF",
    },

    "Camera lock ON": {
        "fr": "Verrouillage caméra ON",
        "en": "Camera lock ON",
    },
    "Camera lock OFF": {
        "fr": "Verrouillage caméra OFF",
        "en": "Camera lock OFF",
    },
    "Camera lock 10s": {
        "fr": "Verrouillage caméra 10s",
        "en": "Camera lock 10s",
    },
    "Camera lock 30s": {
        "fr": "Verrouillage caméra 30s",
        "en": "Camera lock 30s",
    },

    "Magic full": {
        "fr": "Magie pleine",
        "en": "Magic full",
    },
    "Magic half": {
        "fr": "Magie à moitié",
        "en": "Magic half",
    },
    "Magic empty": {
        "fr": "Magie vide",
        "en": "Magic empty",
    },
    "Magic (choice)": {
        "fr": "Magie (choix)",
        "en": "Magic (choice)",
    },

    "Bombs emptied": {
        "fr": "Bombes vidées",
        "en": "Bombs emptied",
    },
    "Bombs +5": {
        "fr": "Bombes +5",
        "en": "Bombs +5",
    },

    "Arrows emptied": {
        "fr": "Flèches vidées",
        "en": "Arrows emptied",
    },
    "Arrows +10": {
        "fr": "Flèches +10",
        "en": "Arrows +10",
    },

    "Random item removed (10s)": {
        "fr": "Item aléatoire retiré (10s)",
        "en": "Random item removed (10s)",
    },
    "Random item removed (30s)": {
        "fr": "Item aléatoire retiré (30s)",
        "en": "Random item removed (30s)",
    },
    "Remove item (30s)": {
        "fr": "Retirer un item (30s)",
        "en": "Remove item (30s)",
    },
    "Remove item (60s)": {
        "fr": "Retirer un item (60s)",
        "en": "Remove item (60s)",
    },

    "Sea waves: Off (30s)": {
        "fr": "Vagues : off (30s)",
        "en": "Sea waves: Off (30s)",
    },
    "Sea waves: Medium (30s)": {
        "fr": "Vagues : medium (30s)",
        "en": "Sea waves: Medium (30s)",
    },
    "Sea waves: Big (30s)": {
        "fr": "Vagues : grosses (30s)",
        "en": "Sea waves: Big (30s)",
    },
    "Sea waves: Freak (30s)": {
        "fr": "Vagues : incontrôlables (30s)",
        "en": "Sea waves: Freak (30s)",
    },
}


def set_lang(lang: str) -> None:
    global _LANG
    if lang in ("fr", "en"):
        _LANG = lang


def get_lang() -> str:
    return _LANG


def tr(text: str) -> str:
    data = _STRINGS.get(text)
    if not data:
        return text
    return data.get(_LANG, text)
