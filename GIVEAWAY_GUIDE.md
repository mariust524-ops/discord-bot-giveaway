# Guide d'Utilisation - Bot Discord Giveaway

## 🎁 Fonctionnalités

Ce bot Discord offre un système de giveaway (cadeaux) complet avec:
- ✅ Commande `/creategiveaway` pour créer des giveaways
- ✅ Système de réaction automatique pour participer
- ✅ Terminaison automatique des giveaways
- ✅ Sélection aléatoire de gagnants
- ✅ Compatibilité avec YouTube et Twitch

---

## 📋 Commandes Slash

### 1️⃣ `/creategiveaway`
Crée un nouveau giveaway sur le serveur.

**Paramètres:**
- `prize` (obligatoire) - Le prix du giveaway (ex: "PlayStation 5", "1000€")
- `duration_minutes` (obligatoire) - Durée en minutes (1 à 10080 = 7 jours max)
- `reaction_emoji` (optionnel) - Emoji pour participer (défaut: 🎉)

**Exemple:**
```
/creategiveaway prize:PlayStation 5 duration_minutes:60 reaction_emoji:🎉
```

**Résultat:** Un message embed est envoyé avec le prix et les instructions. Les utilisateurs réagissent avec l'emoji pour participer.

---

### 2️⃣ `/endgiveaway`
Termine immédiatement un giveaway et sélectionne un gagnant.

**Paramètres:**
- `message_id` (obligatoire) - L'ID du message du giveaway

**Exemple:**
```
/endgiveaway message_id:1234567890123456789
```

---

### 3️⃣ `/giveaways`
Liste tous les giveaways actuellement actifs.

**Exemple:**
```
/giveaways
```

**Affiche:** La liste des giveaways avec le nombre de participants et le temps restant.

---

## 🔧 Configuration

Vous pouvez fournir le token de deux manières :

1. Fichier `config.json` (ci-dessous)
2. Variable d'environnement `DISCORD_TOKEN` (utile pour la sécurité)

```json
{
  "discord_token": "VOTRE_TOKEN_BOT",
  "discord_channel_id": "ID_DU_CHANNEL",
  "youtube_channels": [],
  "twitch_users": [],
  "twitch_client_id": "optionnel",
  "twitch_client_secret": "optionnel",
  "poll_interval": 60
}
```

---

## 👥 Système de Participation

### Comment participer:
1. Un administrateur utilise `/creategiveaway` pour créer un giveaway
2. Les utilisateurs voient un message embed avec le prix
3. Ils réagissent avec l'emoji spécifié pour participer
4. Ils reçoivent une confirmation en DM (optionnel)

### Comment terminer:
- ✅ **Automatique:** Le giveaway se termine après le temps imparti
- ✅ **Manuel:** Un admin utilise `/endgiveaway message_id`

### Sélection du gagnant:
- Le gagnant est choisi **aléatoirement** parmi tous les participants
- Le gagnant est notifié par DM
- Le message du giveaway est mis à jour avec le résultat

---

## 🛡️ Permissions Requises

Pour créer/terminer un giveaway, l'utilisateur doit:
- ✅ Être administrateur du serveur
- ✅ Le bot doit avoir les permissions de:
  - Lire les messages
  - Envoyer les messages
  - Ajouter des réactions
  - Modifier les messages

---

## 📂 Fichiers Générés

Le bot crée automatiquement:

### `giveaways.json`
Stocke tous les giveaways (actifs et terminés) avec:
- Les participants
- Le prix
- Le temps de fin
- L'emoji de réaction
- Le statut (active/finished)

---

## ⚙️ Notes Importantes

1. **Durée maximale:** 10080 minutes (7 jours)
2. **Réactions:** Seul l'emoji spécifié compte pour participer
3. **Retrait de réaction:** Les utilisateurs peuvent retirer leur réaction pour se désinscrire
4. **Données persistantes:** Tous les giveaways sont sauvegardés dans `giveaways.json`
5. **Vérification toutes les minutes:** Les giveaways terminés sont traités automatiquement

---

## 🐛 Troubleshooting

**Le bot n'affiche pas les commandes slash?**
- Attendez quelques secondes après le démarrage
- Le bot doit se synchroniser avec Discord

**Les réactions ne fonctionnent pas?**
- Vérifiez que le bot a la permission d'ajouter des réactions
- Assurez-vous que c'est le bon emoji

**Les participants ne sont pas ajoutés?**
- Vérifiez le fichier `giveaways.json`
- Vérifiez les logs du bot pour les erreurs

---

## 💡 Exemples d'Utilisation

### Giveaway Simple (1 heure)
```
/creategiveaway prize:Cadeau d'une valeur de 50€ duration_minutes:60
```

### Giveaway Long Terme (7 jours avec emoji personnalisé)
```
/creategiveaway prize:Abonnement Premium annuel duration_minutes:10080 reaction_emoji:✨
```

### Terminer un Giveaway Tôt
```
/endgiveaway message_id:1234567890123456789
```

---

Bon giveaway! 🎉
