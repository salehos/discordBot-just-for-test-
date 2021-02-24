import os
import discord

from discord.ext import commands
from dotenv import load_dotenv

conn = sqlite3.connect('test.db')
cur = conn.cursor()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def has_been_delevered (message):
    response = "your message has been delivered"
    return(response)

def reserved_before(message):
    response = "you reserved a request before"
    return (response)

bot = commands.Bot(command_prefix='$')

@bot.command(name= "request", help = "($request [question number] : [question text]) for request mentor for question FOR MEMBERS")
async def question_request(ctx):
    response = "There is a problem"
    notexist = True
    inputstr = str(ctx.message.content).replace("$request", "")
    question_number_and_text = inputstr.split(":")
    question_number = int(question_number_and_text[0])
    group_number = str(ctx.message.channel)
    group_number = group_number.split("-")
    group_number = group_number[1:]
    gp_number = int(group_number[0])
    question_text = ""
    if len(b)>1:
        question_text = str(question_number_and_text[1:])
    rows = cur.execute("SELECT group_id,question_number FROM webelopers").fetchall()
    for row in rows:
        if row[0]==gp_number and row[1]==question_number:
            notexist = False
    if notexist:
        cur.execute("INSERT INTO webelopers(group_id,question_number,reserve,msg) VALUES(?, ? , 0 ,?)",(gp_number,question_number,question_text))
        await ctx.message.channel.send(has_been_delevered(ctx.message))
    else:
        await ctx.message.channel.send(reserved_before(ctx.message))
# this method is for handling user requests
# @bot.command(name= "request", help = "($request [question number]) for request mentor for question FOR MEMBERS")
# async def question_request(ctx):
#     response = "There is a problem"
#     number_of_question = str(ctx.message.content)
#     number_of_question = number_of_question.replace("$request ", "")
#     my_list = open("list.txt", "r+")
#     request_list = my_list.read()
#     my_list.close()
#     if (str(ctx.message.channel) == "group-1") and ("request" in str(ctx.message.content)):
#         if f"question =  {number_of_question}    group = group-1    mark=notreserved" not in request_list :
#             messages = "question = " +  str(ctx.message.content).replace("$request", "")
#             messages += "    " + "group = group-1    mark=notreserved\n"
#             my_list = open("list.txt" , "a+")
#             my_list.write(messages)
#             my_list.flush()
#             my_list.close()
#             await ctx.message.channel.send(has_been_delevered(ctx.message))
#         else:
#             await ctx.message.channel.send(reserved_before(ctx.message))
#
#
#     elif (str(ctx.message.channel) == "group-2") and ("request" in str(ctx.message.content)):
#         if f"question =  {number_of_question}    group = group-2    mark=notreserved" not in request_list:
#             messages = "question = " + str(ctx.message.content).replace("$request","")
#             messages += "    " + "group = group-2    mark=notreserved\n"
#             my_list = open("list.txt", "a+")
#             my_list.write(messages)
#             my_list.flush()
#             my_list.close()
#             await ctx.message.channel.send(has_been_delevered(ctx.message))
#         else:
#             await ctx.message.channel.send(reserved_before(ctx.message))


#this method is for handling mentor requests and give them the last request
@bot.command(name= "solve", help = "($solve for solving problems and requests, FOR MENTORS")
async def solve_request(ctx):
    if "Staff" in str(ctx.message.author.roles):
        solver_staff = str(ctx.message.author)
        rows = cur.execute("SELECT id,group_id,question_number,reserve,mentor_list FROM webelopers WHERE reserve=0;").fetchall()
        match_case_id = -1
        for row in rows:
            if row[4]!=None and solver_staff not in row[4]:
                match_case_id = row[0]
                group_id = row[1]
                question_number = row[2]
                mentor_list = row[4]
                break
        await ctx.message.channel.send(f"you must solve question number {question_number} for group number {group_id}")
        if mentor_list == None:
            mentor_list=""
        mentor_list = str(mentor_list)
        mentor_list += solver_staff+", "
        cur.execute("UPDATE webelopers SET reserve=? AND mentor_list=? WHERE id=?",(1, mentor_list, match_case_id))
    else:
        await ctx.message.channel.send("you have not that permission to do this")
# @bot.command(name= "solve", help = "($solve for solving problems and requests, FOR MENTORS")
# async def solve_request(ctx):
#     if "MENTOR" in str(ctx.message.author.roles):
#         my_list = open("list.txt", "r")
#         lines = my_list.readlines()
#         my_list.close()
#         i = 0
#         for line in lines:
#             if "mark=notreserved" in line:
#                break
#             i += 1
#         await ctx.message.channel.send(lines[i])
#         lines[i] = lines[i].replace("notreserved",'reserved')
#         new_file = open("list.txt", "w+")
#         for line in lines:
#             new_file.write(line)
#         new_file.close()
#
#     else:
#         responce = "YOU HAVE NOT MENTOR PERMISSION BITCH!"
#         await ctx.message.channel.send(responce)


#this method is for solved requests that has been taken by mentors
@bot.command(name= "solved", help = "($solved question_number group_number) for solved problems, FOR MENTORS")
async def solved_request(ctx):
    if "Staff" in str(ctx.message.author.roles):
        message = str(ctx.message.content)
        message = message.replace("$solved ", "")
        question_and_number = message.split(" ")
        question_number = question_and_number[0]
        group_id = question_and_number[1]
        cur.execute("DELETE FROM webelopers WHERE group_id=? AND question_number=?",(group_id,question_number))
        await ctx.message.channel.send("Done!")
# @bot.command(name= "solved", help = "($solved question number group for solved problems, FOR MENTORS")
# async def solved_request(ctx):
#     if "MENTOR" in str(ctx.message.author.roles):
#         message = str(ctx.message.content)
#         message = message.replace("$solved ", "")
#         question_and_number = message.split(" ")
#         requested_questions = open("list.txt","r+")
#         requested_list = requested_questions.readlines()
#         requested_questions.close()
#         message = f"question =  {str(question_and_number[0])}    group = group-{str(question_and_number[1])}    mark=reserved"
#         message2 = f"question =  {str(question_and_number[0])}    group = group-{str(question_and_number[1])}    mark=notreserved"
#         found_message = False
#         if (str(message) in str(requested_list)) or (str(message2) in str(requested_list)) :
#             channel_message = message.replace("mark=reserved","solved ^_^ CONGRATULATIONS")
#             await ctx.message.channel.send(str(channel_message))
#             i = 0
#             for line in requested_list:
#                 if (str(message2) or str(message)) in str(line):
#                     found_message = True
#                     break
#                 i += 1
#             del requested_list[i]
#             new_requested_file = open("list.txt", "w+")
#             for line in requested_list:
#                 new_requested_file.write(line)
#             new_requested_file.close()
#         else:
#             if not found_message:
#                 await ctx.message.channel.send("there is no reserved question for this group and this question")


# this methos is for requests that has been not solved!?
@bot.command(name="notsolved", help="($unsolved questionnumber group for unsolved problems, FOR MENTORS")
async def unsolved_request(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        message = str(ctx.message.content)
        message = message.replace("$notsolved ", "")
        question_and_number = message.split(" ")
        requested_questions = open("list.txt","r+")
        requested_list = requested_questions.readlines()
        requested_questions.close()
        message = f"question =  {str(question_and_number[0])}    group = group-{str(question_and_number[1])}    mark=reserved"
        found_message = False
        if str(message) in str(requested_list) :
            await ctx.message.channel.send(str(message) + "\nchanged to \n")
            channel_message = message.replace("reserved","notreserved")
            await ctx.message.channel.send(str(channel_message))
            i = 0
            for line in requested_list:
                if message in line:
                    found_message = True
                    break
                i += 1
            requested_list[i] = requested_list[i].replace("reserved","notreserved")
            new_requested_file = open("list.txt", "w+")
            for line in requested_list:
                new_requested_file.write(line)
            new_requested_file.close()
        else:
            if not found_message:
                await ctx.message.channel.send("there is no reserved question for this group and this question")
    else:
        await ctx.message.channel.send("you have not that permission")





#for showing all reserved requests
@bot.command(name="showreserved", help="($showreseved) for showing unsolved and reserved questions, FOR MENTORS")
async def showreserved(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        reserved_questions = open("list.txt", "r+")
        reserved_list = reserved_questions.readlines()
        reserved_questions.close()
        is_there_reserve = False
        for line in reserved_list:
            if "mark=reserved" in str(line):
                is_there_reserve = True
                await ctx.message.channel.send(line)
        if not is_there_reserve:
            await ctx.message.channel.send("there is no reserved question")
    else:
        await ctx.message.channel.send("you have not that permission!")


#for showing all unreserved requests
@bot.command(name="showrequests", help="($showrequests) for showing all unreserved questions, FOR MENTORS")
async def showrequests(ctx):
    if "MENTOR" in str(ctx.message.author.roles):
        reserved_questions = open("list.txt", "r+")
        reserved_list = reserved_questions.readlines()
        reserved_questions.close()
        is_there_request = False
        for line in reserved_list:
            if "mark=notreserved" in str(line):
                is_there_request = True
                await ctx.message.channel.send(line)
        if not is_there_request:
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
