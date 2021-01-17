import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def has_been_delevered (message):
    response = "your message has been delivered"
    return(response)

def reserved_before(message):
    response = "you reserved a request before"
    return (response)



bot = commands.Bot(command_prefix='$')

@bot.command(name= "request", help = "($request [question number]) for request mentor for special question FOR MEMBERS")
async def question_request(ctx):
    response = "There is a problem"
    numberOfQuestion = str(ctx.message.content)
    numberOfQuestion = numberOfQuestion.replace("$request ", "")
    print(numberOfQuestion)
    myList = open("list.txt", "r+")
    request_list = myList.read()
    myList.close()
    if (str(ctx.message.channel) == "group-1") and ("request" in str(ctx.message.content)):
        if f"question =  {numberOfQuestion}    group = group-1" not in request_list :
            messages = "question = " +  str(ctx.message.content).replace("$request", "")
            messages += "    " + "group = group-1\n"
            myList = open("list.txt" , "a+")
            myList.write(messages)
            myList.flush()
            myList.close()
            await ctx.message.channel.send(has_been_delevered(ctx.message))
        else:
            await ctx.message.channel.send(reserved_before(ctx.message))


    elif (str(ctx.message.channel) == "group-2") and ("request" in str(ctx.message.content)):
        if f"question =  {numberOfQuestion}    group = group-2" not in request_list:
            messages = "question = " + str(ctx.message.content).replace("$request","")
            messages += "    " + "group = group-2\n"
            myList = open("list.txt", "a+")
            myList.write(messages)
            myList.flush()
            myList.close()
            await ctx.message.channel.send(has_been_delevered(ctx.message))
        else:
            await ctx.message.channel.send(reserved_before(ctx.message))

@bot.command(name= "solve", help = "($solve for solving problems and requests, FOR MENTORS")
async def solve_request(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        myList = open("list.txt", "r")
        lines = myList.readlines()
        myList.close()
        await ctx.message.channel.send(lines[0])
        del lines[0]
        newFile = open("list.txt", "w+")
        for line in lines:
            newFile.write(line)
        newFile.close()
    else:
        responce = "YOU HAVE NOT MENTOR PERMISSION BITCH!"
        await ctx.message.channel.send(responce)


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)



@client.event
async def on_member_join(member):
    print ("hello")
    await member.create_dm()
    await member.dm_channel.send(
        f'سلام. به سرور دیسکورد مسابقه وبلوپرز خوش آمدید!{member.name}'
    )
bot.run(TOKEN)

# import os
# import discord
# from dotenv import load_dotenv
# from discord.ext import commands
#
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
#
#
#
#
#
# @client.event
# async def on_ready():
#     guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
#     print(f'{client.user.name} has connected to Discord!')
#
#
# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'سلام. به سرور دیسکورد مسابقه وبلوپرز خوش آمدید!{member.name}'
#     )
#
#
#
# client.run(TOKEN)
#
