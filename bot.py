import os
import discord
import sqlite3
from discord.ext import commands

conn = sqlite3.connect('webelopers.db')
cur = conn.cursor()


def has_been_delevered (message):
    response = "your message has been delivered"
    return(response)

def reserved_before(message):
    response = "you reserved a request before"
    return (response)

bot = commands.Bot(command_prefix="-")

# cur.execute("CREATE TABLE IF NOT EXISTS webelopers(id integer PRIMARY KEY,group_id integer NOT NULL,msg text NOT NULL,reserve integer NOT NULL, mentor_list text);")

# import sqlite3
# con =sqlite3.connect('webelopers.db')
# cur = con.cursor()
# cur.execute('DELETE FROM webelopers',);
# con.commit()



@bot.command(name= "request", help = "(-request [question text]) for request mentor for a problem || FOR MEMBERS")
async def question_request(ctx):
    print("goes into request")
    response = "There is a problem"
    notexist = True
    inputstr = str(ctx.message.content).replace("-request", "")
    question_text = inputstr
    # question_number = int(question_number_and_text[0])
    group_number = str(ctx.message.channel)
    group_number = group_number.split("-")
    group_number = group_number[1:]
    gp_number = int(group_number[0])
    # question_text = ""
    # if len(question_number_and_text)>1:
    #     question_text = str(question_number_and_text[1:])
    rows = cur.execute("SELECT group_id,msg FROM webelopers").fetchall()
    cur.execute("INSERT INTO webelopers(group_id,msg,reserve) VALUES(?, ? , 0)",(gp_number,question_text))
    conn.commit()
    print("create request")
    await ctx.message.channel.send(has_been_delevered(ctx.message))


#this method is for handling mentor requests and give them the last request
@bot.command(name= "solve", help = "(-solve) for solving problems and requests, FOR MENTORS")
async def solve_request(ctx):
    if "Staff" in str(ctx.message.author.roles):
        print("goes in solve")
        solver_staff = str(ctx.message.author)
        rows = cur.execute("SELECT id,group_id,msg,reserve,mentor_list FROM webelopers WHERE reserve=0;").fetchall()
        if rows == []:
            await ctx.message.channel.send("سوالی برای اختصاص به منتورها وجود ندارد")
            return
        match_case_id = None
        group_id = None
        mentor_list = None
        msg = None
        reserve = None
        for row in rows:
            if (row[4]!=None and solver_staff not in row[4]) or row[4] == None:
                match_case_id = row[0]
                group_id = row[1]
                msg = row[2]
                reserve = row[3]
                mentor_list = row[4]
                break

        await ctx.message.channel.send(f"گروه شماره{group_id}سوالی باشماره آیدی {match_case_id} دارد و سوال آنها به شرح زیر است: {msg}")
        print("did solve")
        if mentor_list == None:
            mentor_list=""
        mentor_list = str(mentor_list)
        mentor_list += solver_staff+", "
        print("----------------------------------------------------------------------")
        print(str(reserve)  +"\n"+ str(mentor_list) +"\n" + str(match_case_id))
        print("----------------------------------------------------------------------")
        cur.execute("UPDATE webelopers set reserve=?,mentor_list=? WHERE id=?",(1,mentor_list, int(match_case_id)))
        conn.commit()
        print("change reserve id")
    else:
        await ctx.message.channel.send("you have not that permission to do this")


#this method is for solved requests that has been taken by mentors
@bot.command(name= "solved", help = "(-solved row.ID) for solved problems, FOR MENTORS")
async def solved_request(ctx):
    if "Staff" in str(ctx.message.author.roles):
        print("goes into solved")
        message = str(ctx.message.content)
        message = message.replace("-solved ", "")
        print(message)
        message = int(message)
        cur.execute("DELETE FROM webelopers WHERE id = ?",(message,))
        conn.commit()
        print("did solved")
        await ctx.message.channel.send("Done!")
    else:
        responce = "YOU HAVE NOT MENTOR PERMISSION!"
        await ctx.message.channel.send(responce)


# this methos is for requests that has been not solved!?
@bot.command(name="unsolved", help="(-unsolved row.ID) for unsolved problems, FOR MENTORS")
async def unsolved_request(ctx):
    if "Staff" in str(ctx.message.author.roles):
        print("goes into unsolved")
        message = str(ctx.message.content)
        message = message.replace("-unsolved ", "")
        message = int(message)
        rows = cur.execute("SELECT id FROM webelopers").fetchall()
        id_list = []
        for row in rows:
            id_list.append(row[0])
        if message not in id_list:
            await ctx.message.channel.send("there is no reserved question for this group and this question")
            return 0
        else:
            cur.execute("UPDATE webelopers SET reserve=? WHERE id=?",(0, message))
            print("back to unsolved problems")
            await ctx.message.channel.send("FIXED!")
            conn.commit()
    else:
        await ctx.message.channel.send("you have not that permission")





#for showing all reserved requests
@bot.command(name="showreserved", help="(-showreseved) for showing unsolved and reserved questions, FOR MENTORS")
async def showreserved(ctx):
    if "Staff" in str(ctx.message.author.roles):
        rows = cur.execute("SELECT group_id,msg FROM webelopers WHERE reserve=1").fetchall()
        if rows != None:
            for row in rows:
                message  = f"group number {row[0]} has a problem with question text {row[1]} and we are working on it"
                await ctx.message.channel.send(message)
        else:
            await ctx.message.channel.send("there is no reserved question")
    else:
        await ctx.message.channel.send("you have not that permission!")



#for showing all unreserved requests
@bot.command(name="showrequests", help="(-showrequests) for showing all unreserved questions, FOR MENTORS")
async def showrequests(ctx):
    if "Staff" in str(ctx.message.author.roles):
        rows = cur.execute("SELECT group_id,msg FROM webelopers WHERE reserve=0").fetchall()
        if rows != None:
            for row in rows:
                message  = f"group number {row[0]} has a problem with question text {row[1]}"
                await ctx.message.channel.send(message)
        else:
            await ctx.message.channel.send("there is question")
    else:
        await ctx.message.channel.send("you have not that permission!")



bot.run(TOKEN)
