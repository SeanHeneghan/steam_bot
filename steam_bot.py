import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="!")

BOT_TOKEN = os.getenv("BOT_TOKEN")

# TODO: Setup basic command to add user steamid record to the database


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx) -> None:
    """Simple method to ping the bot to check it is there."""
    await ctx.send("pong.")


def run_bot() -> None:
    """Basic method to run the bot from outside the module."""
    bot.run(BOT_TOKEN)
