from main import get_summoner_details_message
from discord.ext import commands
import discord
BOT_TOKEN = "MTA2NzgxMTEyODc0MDE1OTU4MA.G00rUw._RSMOQFzI9nCh7nMLHWK8LXsx21imb-ezgGoHU"
CHANNEL_ID = 1067807950745370674

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Naura")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Masnoni")


@bot.command()
async def lolek(ctx, summoner_name):
    result = get_summoner_details_message(summoner_name)
    await ctx.send(result)


bot.run(BOT_TOKEN)
