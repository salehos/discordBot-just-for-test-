import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

def has_been_delevered (message):
    response = "your message has been delivered"
    await message.channel.send(response)

def reserved_before(message):
    response = "you reserved a request before"
    await message.channel.send(response)


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(guild.members)
    for member in guild.members:
        print(member.name)
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    myList = open("list.txt", "r+")
    request_list = myList.read()
    myList.close()
    if message.author == client.user:
        return
    if (str(message.channel) == "group-1") and ("request" in str(message.content)):
        if "group-1" not in request_list :
            messages = message.content + "    " +  "group = group-1\n"
            myList = open("list.txt" , "a+")
            myList.write(messages)
            myList.flush()
            myList.close()
            has_been_delevered(message)
        else :
            reserved_before(message)


    elif (str(message.channel) == "group-2") and ("request" in str(message.content)):
        if "group-2" not in request_list:
            messages = message.content + "    " + "group = group-2\n"
            myList = open("list.txt", "a+")
            myList.write(messages)
            myList.flush()
            myList.close()
            has_been_delevered(message)
        else:
            reserved_before(message)




@client.event
async def on_member_join(member):
    print("worked")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )



client.run(TOKEN)

