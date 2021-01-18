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

@bot.command(name= "request", help = "($request [question number]) for request mentor for question FOR MEMBERS")
async def question_request(ctx):
    response = "There is a problem"
    numberOfQuestion = str(ctx.message.content)
    numberOfQuestion = numberOfQuestion.replace("$request ", "")
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
        reservedQuestions = open("requested.txt","a+")
        reservedQuestions.write(str(lines[0]))
        reservedQuestions.flush()
        reservedQuestions.close()
        del lines[0]
        newFile = open("list.txt", "w+")
        for line in lines:
            newFile.write(line)
        newFile.close()

    else:
        responce = "YOU HAVE NOT MENTOR PERMISSION BITCH!"
        await ctx.message.channel.send(responce)

@bot.command(name= "solved", help = "($solved questionnumber group for solved problems, FOR MENTORS")
async def solved_request(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        message = str(ctx.message.content)
        message = message.replace("$solved ", "")
        questionAndNumber = message.split(" ")
        requestedQuestions = open("requested.txt","r+")
        requestedlist = requestedQuestions.read()
        requestedQuestions.close()
        message = f"question =  {str(questionAndNumber[0])}    group = group-{str(questionAndNumber[1])}"
        if message in requestedlist :
            await ctx.message.channel.send("solved "+ str(message))
            myList = open("requested.txt", "r")
            lines = myList.readlines()
            myList.close()
            i = 0
            for line in lines:
                if message in line:
                    print("found it")
                    break
                i += 1
            del lines[i]
            newRequestedFile = open("requested.txt", "w+")
            for line in lines:
                newRequestedFile.write(line)
            newRequestedFile.close()
        else:
            pass
@bot.command(name="showreserved", help="($showreseved) for showing unsolved and reserved questions, FOR MENTORS")
async def showreserved(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        reservedquestions = open("requested.txt", "r+")
        reservedList = reservedquestions.read()
        reservedquestions.close()
        await ctx.message.channel.send(reservedList)
    else:
        pass
@bot.command(name="showrequests", help="($showrequests) for showing all unreserved questions, FOR MENTORS")
async def showrequests(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        requestedQuestions = open("list.txt", "r+")
        requestedlist = requestedQuestions.read()
        requestedQuestions.close()
        await ctx.message.channel.send(requestedlist)



@bot.command(name="notsolved", help="($unsolved questionnumber group for unsolved problems, FOR MENTORS")
async def unsolved_request(ctx):
    pass

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
