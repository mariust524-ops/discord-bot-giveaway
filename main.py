"""Launcher minimal qui délègue à discord_bot.py.

L'ancien script gérait un client de test ; il n'est plus nécessaire.
Le fichier principal est `discord_bot.py` (où se trouve la classe)
"""

from discord_bot import main as run_bot

if __name__ == "__main__":
    run_bot()
