# Discord announcer bot (YouTube & Twitch)

Ce bot Discord envoie un message dans un canal lorsqu'une nouvelle vidéo YouTube est publiée et lorsqu'un utilisateur commence un stream Twitch.

Installation rapide

1. Copier `config.example.json` en `config.json` et remplir les tokens/IDs.
2. Installer les dépendances:

```bash
pip install -r requirements_bot.txt
```

3. Lancer le bot:

```bash
python discord_bot.py
```

Configuration

- `discord_token`: token du bot Discord
- `discord_channel_id`: id du canal où poster
- `youtube_channels`: liste d'IDs de chaînes YouTube
- `twitch_users`: liste de login Twitch (ex: "shroud")
- `twitch_client_id` / `twitch_client_secret`: pour l'API Twitch
- `poll_interval`: intervalle en secondes entre vérifications

Notes

- Le bot utilise un fichier `state.json` créé automatiquement pour mémoriser le dernier contenu annoncé.
- Pour obtenir l'ID d'une chaîne YouTube, utilisez l'URL de la chaîne (ou recherchez la chaîne et récupérez l'ID).
