from PIL import Image, ImageOps, ImageEnhance, ImageFont, ImageDraw
from pathlib import Path
import discord
import textwrap
import json

def newImage(sender, expression, message, prevsender, side, channel):
    data = json.load(open('data.json'))
    shorthands = data['shorthand']
    names = data['aliases']
    background = data['backgrounds']
    expr_file = (sender + "_" + expression[sender] + ".png")
    try:
        bg = Image.open(background[channel])
    except:
        bg = Image.open("background_awakening.png")
    txtbx = Image.open("vn.png")
    if Path(expr_file).is_file():
        expr = Image.open(expr_file)
    elif expr_file in shorthands:
        expr = Image.open(shorthands[expr_file])
    else:
        expr = Image.open("default.png")
    width1, height1 = bg.size
    width2, height2 = expr.size
    new_height = (height1 - (height1 // 7))
    new_width = new_height * width2 // height2
    expr = expr.resize((new_width, new_height), Image.LANCZOS)
    width2, height2 = expr.size
    height3 = height1 - height2
    if side == True:
        width3 = width1 - width2
        expr = ImageOps.mirror(expr)
    else:
        width3 = 0
    bg.paste(expr, (width3,height3), mask = expr)

    if prevsender != "none":
        expr_file = (prevsender + "_" + expression[prevsender] + ".png")
        if Path(expr_file).is_file():
            expr = Image.open(expr_file)
        elif expr_file in shorthands:
            expr = Image.open(shorthands[expr_file])
        else:
            expr = Image.open("default.png")
        width1, height1 = bg.size
        width2, height2 = expr.size
        new_height = (height1 - (height1 // 7))
        new_width = new_height * width2 // height2
        expr = expr.resize((new_width, new_height), Image.LANCZOS)
        if side == False:
            width3 = width1 - width2
            expr = ImageOps.mirror(expr)
        else:
            width3 = 0
        expr = ImageEnhance.Brightness(expr).enhance(0.5)
        bg.paste(expr, (width3,height3), mask = expr)

    width1, height1 = bg.size
    width2, height2 = txtbx.size
    new_height = width1 * width2 / height2
    new_height = (height1 - (height1 // 7))
    new_width = width1
    txtbx = txtbx.resize((new_width, new_height), Image.LANCZOS)
    width2, height2 = txtbx.size
    height3 = height1 - height2
    width3 = (width1 - width2) // 2
    bg.paste(txtbx, (width3,height3), mask = txtbx)
    dialogue = textwrap.TextWrapper(width=50).fill(text=message)
    ImageDraw.Draw(bg).text((235,865), dialogue, (255,255,255), ImageFont.truetype('font.ttf', 54))
    try:
        name = names[sender]
    except:
        name = ""
    ImageDraw.Draw(bg).text((295,850), name, fill="white", anchor="ms", font=ImageFont.truetype('font.ttf', 45))
    bg.save("test.png")
