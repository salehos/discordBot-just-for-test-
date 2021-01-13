import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    members = ""
    # print(f'{client.user} has connected to Discord!')
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
    f'{client.user} is connected to the following guild:\n'
    f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
        # print(guild.members)

        # for member in guild.members:
        #     print(member.name)




client.run(TOKEN)