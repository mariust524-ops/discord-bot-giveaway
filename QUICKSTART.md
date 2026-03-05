# 🎁 Bot Discord - Système de Giveaway

Un bot Discord complet avec système de giveaway automatisé, réactions et distribution de cadeaux!

## ✨ Fonctionnalités

- **🎁 Giveaways automatisés** - Créez des concours avec durée personnalisée
- **⚡ Système de réaction** - Réagissez avec un emoji pour participer automatiquement
- **🎲 Sélection aléatoire** - Un gagnant est choisi aléatoirement parmi les participants
- **🔔 Notifications** - Les gagnants sont notifiés en DM
- **✅ Synchronisation automatique** - Les giveaways terminés sont traités automatiquement
- **📊 Gestion complète** - Créer, terminer, et lister les giveaways
- **🔐 Permissions** - Seuls les administrateurs peuvent créer des giveaways
- **📺 Compatible** - Fonctionne aussi avec YouTube et Twitch

## 🚀 Installation Rapide

### 1. Cloner/Télécharger
```bash
cd votre_dossier
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer le bot

Le token peut être fourni de deux manières :

1. **Fichier `config.json`** (recommandé) :

```json
{
  "discord_token": "VOTRE_TOKEN_BOT",
  "discord_channel_id": "ID_DU_CHANNEL",
  "youtube_channels": [],
  "twitch_users": [],
  "poll_interval": 60
}
```

2. **Variable d'environnement** :

- Définissez `DISCORD_TOKEN` avant de lancer le bot.
- Cela permet de garder le token hors du repo.

Exemple PowerShell :
```powershell
$env:DISCORD_TOKEN = "votre_token"
python discord_bot.py
```
### 4. Lancer le bot
Le script principal est maintenant `discord_bot.py`. Vous pouvez aussi utiliser

```bash
python main.py  # simple wrapper, équivalent à discord_bot.py
```

> **Relancer le bot**
> - Arrêtez l'exécution en cours (Ctrl+C dans le terminal).
> - Recommencez la commande ci-dessus.
> - Faites cela chaque fois que vous modifiez le code ou la configuration.

## 📖 Commandes Slash

| Commande | Description | Exemple |
|----------|-------------|---------|
| `/creategiveaway` | Créer un nouveau giveaway | `/creategiveaway prize:PS5 duration_minutes:60` |
| `/endgiveaway` | Terminer un giveaway | `/endgiveaway message_id:123456789` |
| `/giveaways` | Lister les giveaways actifs | `/giveaways` |

## 🎯 Flux Utilisateur

```
Admin utilise /creategiveaway
       ↓
Bot envoie message embed avec les infos
       ↓
Bot ajoute la réaction spécifiée
       ↓
Utilisateurs réagissent avec l'emoji
       ↓
Participants sont enregistrés automatiquement
       ↓
Après la durée (ou /endgiveaway):
       ↓
Un gagnant est choisi aléatoirement
       ↓
Message mis à jour + notification au gagnant
```

## 📋 Comment Utiliser

### Créer un Giveaway Simple
1. Tapez `/creategiveaway`
2. Remplissez:
   - **prize**: Le prix (ex: "PlayStation 5")
   - **duration_minutes**: Durée en minutes (ex: 60)
3. Optionnel: Changez l'emoji de réaction

### Participer
1. Voyez le message du giveaway
2. Réagissez avec l'emoji pour participer
3. Attendez la fin et la sélection du gagnant

### Terminer Manuellement
1. Obtenez l'ID du message (clic droit → Copier l'ID du message)
2. Tapez `/endgiveaway message_id:VOTRE_ID`

## 📁 Structure des Fichiers

```
discord_bot.py          # Le bot principal
config.json            # Configuration (créez-le)
giveaways.json         # Données des giveaways (auto-créé)
state.json             # État des vérifications (auto-créé)
requirements.txt       # Dépendances Python
GIVEAWAY_GUIDE.md      # Guide détaillé
```

## ⚙️ Configuration

### config.json obligatoire

```json
{
  "discord_token": "YOUR_BOT_TOKEN_HERE",
  "discord_channel_id": "123456789",
  "youtube_channels": [],
  "twitch_users": [],
  "poll_interval": 60
}
```

- **discord_token**: Token du bot Discord
- **discord_channel_id**: ID du channel par défaut
- **youtube_channels**: Liste des chaînes YouTube à surveiller
- **twitch_users**: Liste des utilisateurs Twitch à surveiller
- **poll_interval**: Intervalle de vérification en secondes

## 🔐 Permissions Requises

Le bot doit avoir ces permissions:
- ✅ Lire les messages
- ✅ Envoyer les messages
- ✅ Ajouter les réactions
- ✅ Modifier les messages
- ✅ Gérer les messages

## 🛠️ Obtenir votre Token Discord

1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez "New Application"
3. Onglet "Bot" → "Add Bot"
4. Copier le TOKEN
5. Coller dans config.json

## ⏰ Limitations

- Durée maximale: 10080 minutes (7 jours)
- Durée minimale: 1 minute
- Un emoji par giveaway
- Seuls les administrateurs peuvent créer des giveaways

## 🐛 Problèmes Courants

**"discord_token manquant"**
- Vous avez oublié de créer `config.json`
- Ou le token manque dans la configuration

**Les commandes slash n'apparaissent pas**
- Attendez quelques secondes après le démarrage
- Le bot doit se synchroniser avec Discord

**Les réactions ne fonctionnent pas**
- Vérifiez que le bot a la permission d'ajouter des réactions

## 📞 Support

Pour plus d'informations, consultez `GIVEAWAY_GUIDE.md`

## 📝 Licence

Libre d'utilisation et de modification

---

**Bon giveaway! 🎉**
