# import os
import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = "Nzk4MjM5OTQ0MzY3MTQ0OTcw.X_yI4Q.SwQkhiCxPZ1p9LsarNU2bZGFg14"
GUILD = "Meeting and Jalase."


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    for member in guild.members:
        print(member.name)
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    print("worked")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )



client.run(TOKEN)

