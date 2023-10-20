import discord
from discord.ext import commands
import random
import pytz


paris = pytz.timezone('Europe/paris')

TOKEN = "MTE2NDY2MzUwMDc2NTkyMTQ5MQ.Gp0cg-.gqhtXbuwuFMOd_UKj-NuQ3GzUQzInD4uw3a_hw"


number = 0
found = True

# Intents (intentions)
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True

bot = commands.Bot(command_prefix='!', description="J-Test bot", intents=intents)

def log(msg):
    print(f"{msg.message.created_at.astimezone(paris).strftime('%H:%M:%S %d/%m/%Y')} [{msg.author}({msg.author.id})")

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.command()
async def ping(ctx):
    """Retourn toujour "Pong !" """
    log(ctx)
    await ctx.send("Pong !")

@bot.command()
async def jeu(ctx):
    """
    Envoi le lien des jeux
    """
    data = """Liens: \n1. https://garticphone.com/fr\n2. https://jklm.fun/"""
    await ctx.send(data)

@bot.command()
async def guess(ctx, args=None):
    """
    Jouer au Jeu du plus-moins
    """
    global number, found
    if args == None:
        if not found:
            await ctx.send("`!guess <int>` pour faire un guess")
            return
        await ctx.send("`!guess start` pour commencer une nouvelle partie")
        return
    if args == "start" or found:
        number = random.randint(0, 100)
        found = False
        print(number)
        await ctx.send("Trouvez le nombre entre 0 et 100")
        return
    try:
        guess = int(args)
    except Exception as e:
        await ctx.send("Merci de rentrer un nombre valide")
    if guess == number:
        found = True
        await ctx.send("Trouvé !!")

    if number > guess :
        await ctx.send("Plus")
        return
    if number < guess :
        await ctx.send("Moins")
        return


# @bot.event
# async def on_message(msg):
#     if msg.content.lower().endswith(" quoi") or msg.content.lower() == "quoi" :
#         await msg.channel.send("feur")
#     if msg.content.lower() == "ok":
#         await msg.channel.send("boomer")

# Remplacez "YOUR_TOKEN_HERE" par le token de votre bot
bot.run(TOKEN)
