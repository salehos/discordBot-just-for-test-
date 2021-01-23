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


# this method is for handling user requests
@bot.command(name= "request", help = "($request [question number]) for request mentor for question FOR MEMBERS")
async def question_request(ctx):
    response = "There is a problem"
    numberOfQuestion = str(ctx.message.content)
    numberOfQuestion = numberOfQuestion.replace("$request ", "")
    myList = open("list.txt", "r+")
    request_list = myList.read()
    myList.close()
    if (str(ctx.message.channel) == "group-1") and ("request" in str(ctx.message.content)):
        if f"question =  {numberOfQuestion}    group = group-1    mark=notreserved" not in request_list :
            messages = "question = " +  str(ctx.message.content).replace("$request", "")
            messages += "    " + "group = group-1    mark=notreserved\n"
            myList = open("list.txt" , "a+")
            myList.write(messages)
            myList.flush()
            myList.close()
            await ctx.message.channel.send(has_been_delevered(ctx.message))
        else:
            await ctx.message.channel.send(reserved_before(ctx.message))


    elif (str(ctx.message.channel) == "group-2") and ("request" in str(ctx.message.content)):
        if f"question =  {numberOfQuestion}    group = group-2    mark=notreserved" not in request_list:
            messages = "question = " + str(ctx.message.content).replace("$request","")
            messages += "    " + "group = group-2    mark=notreserved\n"
            myList = open("list.txt", "a+")
            myList.write(messages)
            myList.flush()
            myList.close()
            await ctx.message.channel.send(has_been_delevered(ctx.message))
        else:
            await ctx.message.channel.send(reserved_before(ctx.message))


#this method is for handling mentor requests and give them the last request
@bot.command(name= "solve", help = "($solve for solving problems and requests, FOR MENTORS")
async def solve_request(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        myList = open("list.txt", "r")
        lines = myList.readlines()
        myList.close()
        i = 0
        for line in lines:
            if "mark=notreserved" in line:
               break
            i += 1
        await ctx.message.channel.send(lines[i])
        lines[i] = lines[i].replace("notreserved",'reserved')
        newFile = open("list.txt", "w+")
        for line in lines:
            newFile.write(line)
        newFile.close()

    else:
        responce = "YOU HAVE NOT MENTOR PERMISSION BITCH!"
        await ctx.message.channel.send(responce)


#this method is for solved requests that has been taken by mentors
@bot.command(name= "solved", help = "($solved questionnumber group for solved problems, FOR MENTORS")
async def solved_request(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        message = str(ctx.message.content)
        message = message.replace("$solved ", "")
        questionAndNumber = message.split(" ")
        requestedQuestions = open("list.txt","r+")
        requestedlist = requestedQuestions.readlines()
        requestedQuestions.close()
        for line in requestedlist:
            if "\n" in line:
                line = line.replace("\n","")
        message = f"question =  {str(questionAndNumber[0])}    group = group-{str(questionAndNumber[1])}    mark=reserved"
        foundMessage = False
        if message in requestedlist :
            print("FUCKOFF")
            channelMessage = message.replace("reserved","solved")
            await ctx.message.channel.send(str(channelMessage))
            i = 0
            for line in requestedlist:
                if message in line:
                    b = True
                    print("found it")
                    break
                i += 1

            del requestedlist[i]
            newRequestedFile = open("list.txt", "w+")
            for line in requestedlist:
                newRequestedFile.write(line)
            newRequestedFile.close()
        else:
            if not foundMessage:
                await ctx.message.channel.send("there is no reserved question for this group and this question")


# this methos is for requests that has been not solved!?
@bot.command(name="notsolved", help="($unsolved questionnumber group for unsolved problems, FOR MENTORS")
async def unsolved_request(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        message = str(ctx.message.content)
        message = message.replace("$notsolved ", "")
        questionAndNumber = message.split(" ")
        requestedQuestions = open("list.txt","r+")
        requestedlist = requestedQuestions.readlines()
        requestedQuestions.close()
        for line in requestedlist:
            if "\n" in line:
                line = line.replace("\n", "")
        message = f"question =  {str(questionAndNumber[0])}    group = group-{str(questionAndNumber[1])}    mark=reserved"
        foundMessage = False
        if message in requestedlist :
            print("FUCKOFF")
            channelMessage = message.replace("reserved","notreserved")
            await ctx.message.channel.send(str(channelMessage))
            i = 0
            for line in requestedlist:
                print(message)
                print(line)
                if message in line:
                    foundMessage = True
                    break
                i += 1
            requestedlist[i] = requestedlist[i].replace("reserved","notreserved")
            newRequestedFile = open("list.txt", "w+")
            for line in requestedlist:
                newRequestedFile.write(line)
            newRequestedFile.close()
        else:
            if not foundMessage:
                await ctx.message.channel.send("there is no reserved question for this group and this question")
    else:
        await ctx.message.channel.send("you have not that permission")





#for showing all reserved requests
@bot.command(name="showreserved", help="($showreseved) for showing unsolved and reserved questions, FOR MENTORS")
async def showreserved(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        reservedquestions = open("list.txt", "r+")
        reservedList = reservedquestions.readlines()
        reservedquestions.close()
        isThereReserve = False
        for line in reservedList:
            if "mark=reserved" in str(line):
                isThereReserve = True
                await ctx.message.channel.send(line)
        if not isThereReserve:
            await ctx.message.channel.send("there is no reserved question")
    else:
        await ctx.message.channel.send("you have not that permission!")


#for showing all unreserved requests
@bot.command(name="showrequests", help="($showrequests) for showing all unreserved questions, FOR MENTORS")
async def showrequests(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        reservedquestions = open("list.txt", "r+")
        reservedList = reservedquestions.readlines()
        reservedquestions.close()
        isThereRequest = False
        for line in reservedList:
            if "mark=notreserved" in str(line):
                isThereRequest = True
                await ctx.message.channel.send(line)
        if not isThereRequest:
            await ctx.message.channel.send("there is no request")
    else:
        await ctx.message.channel.send("you have not that permission!")


bot.run(TOKEN)

#
# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)
#
#
#
# @client.event
# async def on_member_join(member):
#     print ("hello")
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'سلام. به سرور دیسکورد مسابقه وبلوپرز خوش آمدید!{member.name}'
#     )

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
