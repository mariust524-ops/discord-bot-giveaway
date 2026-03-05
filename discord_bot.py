# Workaround: ensure the standard 'types' module is used (avoids conflict with discord.types on Python 3.14)
import sys
import types as _stdlib_types
sys.modules.setdefault('types', _stdlib_types)

import asyncio
import json
import os
import time
import random
from typing import Dict, Any, List

import aiohttp

# optional dependency for YouTube RSS checks; install via pip or requirements.txt
try:
    import feedparser
except ImportError:
    feedparser = None
    print("⚠️ Module 'feedparser' non installé. Installez-le avec 'pip install feedparser' ou 'pip install -r requirements.txt'.")

import discord
from discord.ext import commands, tasks
from discord import app_commands

# Le token ne doit pas être codé en dur dans le fichier.
# Placez le token dans config.json (champ "discord_token")
# ou dans la variable d'environnement DISCORD_TOKEN.
# Le chemin du fichier de configuration est défini ci-dessous.

CONFIG_PATH = "config.json"  # voir ci-dessus
STATE_PATH = "state.json"
GIVEAWAYS_PATH = "giveaways.json"


def load_json(path: str, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class GiveawayBot(commands.Bot):
    def __init__(self, config: Dict[str, Any], *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        # use 'reactions' intent (not 'reaction')
        intents.reactions = True
        super().__init__(intents=intents, command_prefix="!", *args, **kwargs)
        self.config = config
        self.state = load_json(STATE_PATH, {"youtube": {}, "twitch": {}, "twitch_token": None, "twitch_token_time": 0})
        self.giveaways = load_json(GIVEAWAYS_PATH, {})
        # postpone HTTP session until after the event loop is running
        self.session = None
        self.bg_task = None

    async def on_ready(self):
        print(f"Connecté en tant que {self.user} (id: {self.user.id})")
        try:
            synced = await self.tree.sync()
            print(f"{len(synced)} commandes slash synchronisées")
        except Exception as e:
            print(f"Erreur synchronisation slash commands: {e}")

        # create aiohttp session now that loop is running
        if self.session is None:
            self.session = aiohttp.ClientSession()

        # Démarrer la boucle de vérification des giveaways
        self.giveaway_check.start()

        # lancer la boucle background (polling) si elle n'est pas déjà lancée
        if self.bg_task is None:
            try:
                self.bg_task = self.loop.create_task(self.background_loop())
            except Exception:
                # fallback: ignore if we cannot create the task
                self.bg_task = None

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Gère l'ajout de réaction pour participer aux giveaways"""
        if user.bot:
            return
        
        # Vérifier si c'est un giveaway
        message_id = str(reaction.message.id)
        if message_id not in self.giveaways:
            return
        
        giveaway = self.giveaways[message_id]
        if giveaway.get("status") != "active":
            return
        
        # Ajouter l'utilisateur à la liste des participants
        if "participants" not in giveaway:
            giveaway["participants"] = []
        
        user_id = str(user.id)
        if user_id not in giveaway["participants"]:
            giveaway["participants"].append(user_id)
            save_json(GIVEAWAYS_PATH, self.giveaways)
            # Optionnel: message de confirmation
            try:
                await user.send(f"✅ Vous avez participé au giveaway: **{giveaway['prize']}**")
            except:
                pass

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        """Gère le retrait de réaction"""
        if user.bot:
            return
        
        message_id = str(reaction.message.id)
        if message_id not in self.giveaways:
            return
        
        giveaway = self.giveaways[message_id]
        user_id = str(user.id)
        
        if "participants" in giveaway and user_id in giveaway["participants"]:
            giveaway["participants"].remove(user_id)
            save_json(GIVEAWAYS_PATH, self.giveaways)

    @tasks.loop(minutes=1)
    async def giveaway_check(self):
        """Vérifie et termine les giveaways qui ont expiré"""
        current_time = time.time()
        giveaways_to_remove = []
        
        for message_id, giveaway in self.giveaways.items():
            if giveaway.get("status") != "active":
                continue
            
            if current_time >= giveaway["end_time"]:
                # Terminer le giveaway
                channel_id = giveaway["channel_id"]
                channel = self.get_channel(channel_id)
                
                if channel and giveaway.get("message_id"):
                    try:
                        message = await channel.fetch_message(int(message_id))
                        await self.finish_giveaway(message, giveaway)
                    except Exception as e:
                        print(f"Erreur lors de la finition du giveaway: {e}")
                
                giveaway["status"] = "finished"
                giveaways_to_remove.append(message_id)
        
        if giveaways_to_remove or any(g.get("status") == "finished" for g in self.giveaways.values()):
            save_json(GIVEAWAYS_PATH, self.giveaways)

    @giveaway_check.before_loop
    async def before_giveaway_check(self):
        await self.wait_until_ready()

    async def finish_giveaway(self, message: discord.Message, giveaway: Dict[str, Any]):
        """Termine un giveaway et sélectionne un gagnant"""
        participants = giveaway.get("participants", [])
        
        if not participants:
            embed = discord.Embed(
                title=f"🎁 {giveaway['prize']}",
                description="Aucun participant... Pas de gagnant!",
                color=discord.Color.red()
            )
            try:
                await message.edit(embed=embed)
            except:
                pass
            return
        
        # Sélectionner un gagnant aléatoire
        winner_id = random.choice(participants)
        try:
            winner = await self.fetch_user(int(winner_id))
        except:
            winner = None
        
        # Créer l'embed du résultat
        embed = discord.Embed(
            title=f"🎉 {giveaway['prize']}",
            description=f"**Gagnant:** {winner.mention if winner else f'<@{winner_id}>'}\n\n✅ Giveaway terminé!",
            color=discord.Color.gold()
        )
        embed.add_field(name="Participants", value=f"{len(participants)}", inline=True)
        
        try:
            await message.edit(embed=embed)
        except:
            pass
        
        # Notifier le gagnant
        if winner:
            try:
                await winner.send(f"🎉 Félicitations! Vous avez gagné **{giveaway['prize']}** sur le serveur!")
            except:
                pass

    @app_commands.command(name="creategiveaway", description="Créer un nouveau giveaway")
    @app_commands.describe(
        prize="Le prix du giveaway",
        duration_minutes="Durée en minutes (1-10080)",
        reaction_emoji="Emoji pour participer (défaut: 🎉)"
    )
    async def create_giveaway(
        self, 
        interaction: discord.Interaction, 
        prize: str,
        duration_minutes: int,
        reaction_emoji: str = "🎉"
    ):
        """Crée un nouveau giveaway avec une durée et un emoji de réaction"""
        
        # Vérification des permissions
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Vous devez être administrateur pour créer un giveaway",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Validation de la durée
        if duration_minutes < 1 or duration_minutes > 10080:  # max 7 jours
            embed = discord.Embed(
                title="❌ Erreur",
                description="La durée doit être entre 1 et 10080 minutes (1 à 7 jours)",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Calculer le temps de fin
        end_time = time.time() + (duration_minutes * 60)
        
        # Créer l'embed du giveaway
        embed = discord.Embed(
            title=f"🎁 {prize}",
            description=f"Réagissez avec {reaction_emoji} pour participer!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Durée", value=f"{duration_minutes} minutes", inline=True)
        embed.add_field(name="Temps restant", value=f"<t:{int(end_time)}:R>", inline=True)
        embed.set_footer(text="Giveaway en cours...")
        
        # Envoyer le message du giveaway
        giveaway_message = await interaction.channel.send(embed=embed)
        
        # Ajouter la réaction
        try:
            await giveaway_message.add_reaction(reaction_emoji)
        except Exception as e:
            print(f"Erreur lors de l'ajout de réaction: {e}")
        
        # Enregistrer le giveaway
        message_id = str(giveaway_message.id)
        self.giveaways[message_id] = {
            "prize": prize,
            "channel_id": interaction.channel_id,
            "message_id": giveaway_message.id,
            "end_time": end_time,
            "reaction_emoji": reaction_emoji,
            "status": "active",
            "participants": []
        }
        save_json(GIVEAWAYS_PATH, self.giveaways)
        
        # Répondre à l'interaction
        embed_response = discord.Embed(
            title="✅ Giveaway créé",
            description=f"Le giveaway pour **{prize}** a été créé avec succès!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed_response, ephemeral=True)

    @app_commands.command(name="endgiveaway", description="Terminer un giveaway immédiatement")
    @app_commands.describe(
        message_id="L'ID du message du giveaway à terminer"
    )
    async def end_giveaway(self, interaction: discord.Interaction, message_id: str):
        """Termine immédiatement un giveaway spécifique"""
        
        # Vérification des permissions
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Vous devez être administrateur pour terminer un giveaway",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if message_id not in self.giveaways:
            embed = discord.Embed(
                title="❌ Erreur",
                description="Ce giveaway n'existe pas",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        giveaway = self.giveaways[message_id]
        channel = self.get_channel(giveaway["channel_id"])
        
        if channel:
            try:
                message = await channel.fetch_message(int(message_id))
                await self.finish_giveaway(message, giveaway)
            except Exception as e:
                print(f"Erreur: {e}")
        
        giveaway["status"] = "finished"
        save_json(GIVEAWAYS_PATH, self.giveaways)
        
        embed_response = discord.Embed(
            title="✅ Giveaway terminé",
            description="Le giveaway a été terminé et un gagnant a été sélectionné!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed_response, ephemeral=True)

    @app_commands.command(name="giveaways", description="Voir tous les giveaways actifs")
    async def list_giveaways(self, interaction: discord.Interaction):
        """Liste tous les giveaways actuellement actifs"""
        
        active_giveaways = {
            msg_id: g for msg_id, g in self.giveaways.items() 
            if g.get("status") == "active"
        }
        
        if not active_giveaways:
            embed = discord.Embed(
                title="📦 Giveaways",
                description="Aucun giveaway actif pour le moment",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📦 Giveaways Actifs",
            color=discord.Color.blue()
        )
        
        for msg_id, giveaway in list(active_giveaways.items())[:10]:  # Max 10
            remaining_time = giveaway["end_time"] - time.time()
            if remaining_time < 0:
                remaining_time = 0
            
            minutes_left = int(remaining_time / 60)
            participants = len(giveaway.get("participants", []))
            
            embed.add_field(
                name=f"🎁 {giveaway['prize']}",
                value=f"Participants: {participants}\nTemps restant: {minutes_left} min\nID: `{msg_id}`",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def close(self):
        """Ferme proprement le bot"""
        # arrêter la loop des giveaways si elle tourne
        try:
            if hasattr(self, 'giveaway_check') and self.giveaway_check.is_running():
                try:
                    self.giveaway_check.stop()
                except Exception:
                    pass
        except Exception:
            pass

        # annuler la tâche background si nécessaire
        if getattr(self, 'bg_task', None):
            try:
                self.bg_task.cancel()
                try:
                    await self.bg_task
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass
            except Exception:
                pass

        # fermer la session aiohttp si elle existe et n'est pas déjà fermée
        if getattr(self, 'session', None):
            try:
                closed_attr = getattr(self.session, 'closed', None)
                if closed_attr is False or closed_attr is None:
                    await self.session.close()
            except Exception:
                pass
            finally:
                self.session = None

        await super().close()

    async def background_loop(self):
        await self.wait_until_ready()
        interval = int(self.config.get("poll_interval", 60))
        while not self.is_closed():
            try:
                await self.check_youtube()
                await self.check_twitch()
            except Exception as e:
                print("Erreur dans la boucle de background:", e)
            await asyncio.sleep(interval)

    async def post_channel(self, message: str):
        channel_id = int(self.config["discord_channel_id"])
        channel = self.get_channel(channel_id)
        if channel is None:
            print(f"Impossible de trouver le channel Discord {channel_id}")
            return
        try:
            await channel.send(message)
        except Exception as e:
            print("Erreur en envoyant le message Discord:", e)

    async def check_youtube(self):
        # if feedparser failed to import, skip YouTube functionality
        if feedparser is None:
            return

        youtube_list: List[str] = self.config.get("youtube_channels", [])
        for ch in youtube_list:
            feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={ch}"
            try:
                async with self.session.get(feed_url) as r:
                    if r.status != 200:
                        print(f"Erreur fetch RSS YouTube {ch}: {r.status}")
                        continue
                    text = await r.text()
                feed = feedparser.parse(text)
                if not feed.entries:
                    continue
                latest = feed.entries[0]
                video_url = latest.get("link")
                video_id = None
                if video_url and "watch?v=" in video_url:
                    video_id = video_url.split("watch?v=")[-1]
                else:
                    video_id = latest.get("id") or latest.get("yt_videoid")

                last = self.state.get("youtube", {}).get(ch)
                if video_id and video_id != last:
                    title = latest.get("title", "Nouvelle vidéo")
                    author = latest.get("author", "YouTube")
                    msg = f"🎬 Nouvelle vidéo de {author} — {title}\n{video_url}"
                    await self.post_channel(msg)
                    self.state.setdefault("youtube", {})[ch] = video_id
                    save_json(STATE_PATH, self.state)
            except Exception as e:
                print("Erreur check_youtube:", e)

    async def get_twitch_token(self):
        now = int(time.time())
        token = self.state.get("twitch_token")
        token_time = int(self.state.get("twitch_token_time", 0))
        # refresh every 50 minutes
        if token and now - token_time < 50 * 60:
            return token

        client_id = self.config.get("twitch_client_id")
        client_secret = self.config.get("twitch_client_secret")
        if not client_id or not client_secret:
            print("Twitch client_id/secret non configurés")
            return None
        url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
        async with self.session.post(url) as r:
            if r.status != 200:
                print("Erreur token Twitch:", r.status)
                return None
            data = await r.json()
            token = data.get("access_token")
            if token:
                self.state["twitch_token"] = token
                self.state["twitch_token_time"] = now
                save_json(STATE_PATH, self.state)
            return token

    async def check_twitch(self):
        twitch_users: List[str] = self.config.get("twitch_users", [])
        if not twitch_users:
            return
        token = await self.get_twitch_token()
        if not token:
            return
        client_id = self.config.get("twitch_client_id")
        headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
        for user in twitch_users:
            try:
                url = f"https://api.twitch.tv/helix/streams?user_login={user}"
                async with self.session.get(url, headers=headers) as r:
                    if r.status == 401:
                        # force refresh next time
                        self.state["twitch_token_time"] = 0
                        save_json(STATE_PATH, self.state)
                        continue
                    if r.status != 200:
                        print(f"Erreur Twitch API {r.status} pour {user}")
                        continue
                    data = await r.json()
                streams = data.get("data", [])
                is_live = len(streams) > 0
                was_live = self.state.get("twitch", {}).get(user, False)
                if is_live and not was_live:
                    s = streams[0]
                    title = s.get("title", "Live Twitch")
                    game = s.get("game_name")
                    url_stream = f"https://twitch.tv/{user}"
                    msg = f"🔴 {user} est en live sur Twitch — {title}"
                    if game:
                        msg += f" — {game}"
                    msg += f"\n{url_stream}"
                    await self.post_channel(msg)
                self.state.setdefault("twitch", {})[user] = bool(is_live)
                save_json(STATE_PATH, self.state)
            except Exception as e:
                print("Erreur check_twitch:", e)


def main():
    if not os.path.exists(CONFIG_PATH):
        print(f"Placez un fichier de configuration '{CONFIG_PATH}'. Voir config.example.json")
        return
    config = load_json(CONFIG_PATH, {})
    # Allow token to be defined in config.json or via environment variable
    token = config.get("discord_token") or os.getenv("DISCORD_TOKEN")
    if not token:
        print("discord_token manquant dans le config.json ou variable d'environnement DISCORD_TOKEN")
        return
    bot = GiveawayBot(config)
    bot.run(token)


if __name__ == "__main__":
    main()
