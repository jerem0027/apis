#!/usr/bin/env python
# -*- coding: utf-8 -*-

colors = {
    "Black":        "0;30",
    "Red":          "0;31",
    "Green":        "0;32",
    "Orange":       "0;33",
    "Blue":         "0;34",
    "Purple":       "0;35",
    "Cyan":         "0;36",
    "Light Gray":   "0;37",
    "Dark Gray":    "1;30",
    "Light Red":    "1;31",
    "Light Green":  "1;32",
    "Yellow":       "1;33",
    "Light Blue":   "1;34",
    "Light Purple": "1;35",
    "Light Cyan":   "1;36",
    "White":        "1;37"
}

def purple(text:str) -> str:
    """Retourne le text en purple

    Args:
        text (str): text que le veut afficher en purple

    Returns:
        str: text entouré des balises lui donnant une couleur purple
    """
    return f"\033[{colors['Purple']}m{text}\033[0m"

def cyan(text:str) -> str:
    """Retourne le text en cyan

    Args:
        text (str): text que le veut afficher en cyan

    Returns:
        str: text entouré des balises lui donnant une couleur cyan
    """
    return f"\033[{colors['Cyan']}m{text}\033[0m"

def green(text:str) -> str:
    """Retourne le text en vert

    Args:
        text (str): text que le veut afficher en vert

    Returns:
        str: text entouré des balises lui donnant une couleur verte
    """
    return f"\033[{colors['Green']}m{text}\033[0m"

def red(text:str) -> str:
    """Retourne le text en rouge

    Args:
        text (str): text que le veut afficher en rouge

    Returns:
        str: text entouré des balises lui donnant une couleur rouge
    """
    return f"\033[{colors['Red']}m{text}\033[0m"

def orange(text:str) -> str:
    """Retourne le text en orange

    Args:
        text (str): text que le veut afficher en orange

    Returns:
        str: text entouré des balises lui donnant une couleur orange
    """
    return f"\033[{colors['Orange']}m{text}\033[0m"