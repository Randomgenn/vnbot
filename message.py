import json
import discord
import re
import os
from pathlib import Path
from image import newImage
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def vn(ctx, arg1=None, arg2=None, arg3=None):
    data = json.load(open('data.json'))
    if arg1 == "delete":
        if arg2 == "portrait":
            if os.path.exists(str(ctx.author.id) + "_" + arg3 + ".png"):
                os.remove(str(ctx.author.id) + "_" + arg3 + ".png")
                await ctx.send("deleted!")
            else:
                await ctx.send("nothin there!")
        elif arg2 == "background":
            if os.path.exists("background_" + arg3 + ".png"):
                os.remove("background_" + arg3 + ".png")
                await ctx.send("deleted!")
            else:
                await ctx.send("nothin there!")
        elif arg2 == "shorthand":
            list = data['shorthand']
            code = (str(ctx.author.id) + "_" + sh + ".png")
            del list[code]
            json.dump(data, open('data.json', 'w'))
    elif arg1 == "add":
        if arg2 == "portrait":
            split_str = arg3.split("<")
            for s in split_str[1:]:
                split_s = s.split(">")
                sh = str(split_s[0])
                print(sh)
            portraitname = (str(ctx.author.id) + "_" + arg3 + ".png")
            await ctx.message.attachments[0].save(portraitname)
            await ctx.send("portrait " + arg3 + " added")
        elif arg2 == "background":
            backgroundname = ("background_" + arg3 + ".png")
            await ctx.message.attachments[0].save(backgroundname)
            await ctx.send("background " + arg3 + " added")
        else:
            await ctx.send("invalid!")
    elif arg1 == "help":
        await ctx.send("""commands: \n>/vn add [*portrait/background*] [*file ID*]
>/vn alias [*name*]
>/vn shorthand [*file ID*] [*alternative keyword*]
>/vn background [*file ID*]
>/vn on
>/vn off
>/vn delete [*portrait/background/shorthand*] [*file ID/shorthand*]

*(note: while in VN mode, you can enter a portrait file ID or shorthand in < > to change the expression)*""")
    elif arg1 == "on":
        vncheck[str(ctx.author.id)] = True
        await ctx.message.add_reaction("✅")
    elif arg1 == "off":
        vncheck[str(ctx.author.id)] = False
        await ctx.message.add_reaction("✅")
    elif arg1 == "shorthand":
        filename = (str(ctx.author.id) + "_" + arg2 + ".png")
        if Path(filename).is_file():
            split_str = arg3.split("<")
            for s in split_str[1:]:
                split_s = s.split(">")
                sh = str(split_s[0])
                print(sh)
            shortname = (str(ctx.author.id) + "_" + sh + ".png")
            shorthand = {shortname : filename}
            data['shorthand'] = shorthand
            json.dump(data, open('data.json', 'w'))
            await ctx.send("shorthand added")
        else:
            await ctx.send("no file with that name")
    elif arg1 == "alias":
        names = data['aliases']
        names[str(ctx.author.id)] = arg2
        json.dump(data, open('data.json', 'w'))
        await ctx.send("name updated!")
    elif arg1 == "background":
        backgrounds = data['backgrounds']
        background = ("background_" + arg2 + ".png")
        print(background)
        backgrounds[str(ctx.channel.id)] = background
        print(backgrounds)
        json.dump(data, open('data.json', 'w'))
        await ctx.send("background updated!")
    else:
        await ctx.send("not a valid command. perish")
    

expr = {}
sender = "none"
prev = "none"
prevsender = "none"
side = False
vncheck = {}

@bot.event
async def on_message(message):
    global expr
    global sender
    global prev
    global prevsender
    global side
    global vncheck
    try:
        vncheck[str(message.author.id)]
    except:
        vncheck[str(message.author.id)] = False
    if str(message.author.id) != '737857796128899153' and vncheck[str(message.author.id)] == True and message.content.startswith("/vn") == False:
        await message.delete()
        prev = sender
        sender = str(message.author.id)
        if prev != sender and prev != "none":
            prevsender = prev
            side = not side
        if (sender in expr) == False:
            expr[sender] = "neutral"
        if message.content != "" :
            split_str = message.content.split("<")
            for s in split_str[1:]:
                split_s = s.split(">")
                expr[str(message.author.id)] = str(split_s[0])
            txt = re.sub("<.*> |<.*>", "", message.content)
            newImage(sender, expr, txt, prevsender, side, str(message.channel.id))
            await message.channel.send(file=discord.File('test.png'))
    await bot.process_commands(message) 

bot.run('token goes here')
