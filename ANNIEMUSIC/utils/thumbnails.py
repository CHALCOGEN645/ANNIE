import os
import re
import textwrap

import aiofiles
import aiohttp
import numpy as np
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch
from ANNIEMUSIC import app

from config import YOUTUBE_IMG_URL,MUSIC_BOT_NAME



def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def circle(img):
    h,w=img.size
    a = Image.new('L', [h,w], 0)
    b = ImageDraw.Draw(a)
    b.pieslice([(0, 0), (h,w)], 0, 360, fill = 255,outline = "white")
    c = np.array(img)
    d = np.array(a)
    e = np.dstack((c, d))
    return Image.fromarray(e)

def circle2(img,Xcenter,Ycenter):
    h,w=img.size
    a = Image.new('L', [h,w], 0)
    b = ImageDraw.Draw(a)
    b.pieslice([(0, 0), (h,w)], 0, 360, fill = 255,outline = "white")
    b.pieslice([(int(Xcenter-50), int(Ycenter-30)), (int(Xcenter+50),int(Ycenter+30))], 0, 360, fill = 0,outline = "black")
    c = np.array(img)
    d = np.array(a)
    e = np.dstack((c, d))
    return Image.fromarray(e)

def squ(img1):
    a = Image.new('L', [640,500], 0)
    b=ImageDraw.Draw(a)
    b.line((320,0,240,550),fill="white",width=670)
    e=Image.fromarray(np.dstack((np.array(img1),np.array(a))))
    return e

async def gen_thumb(videoid,user_id):
    if os.path.isfile(f"cache/{videoid}_{user_id}.png"):
       return f"cache/{videoid}_{user_id}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                   duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()
        p=0            
        try: 
            async for photo in app.get_chat_photos(user_id,1): 
                sp=await app.download_media(photo.file_id, file_name=f'{user_id}.jpg')
                p=1
            if p==0:
                raise Exception
        except: 
            async for photo in app.get_chat_photos(app.id,1): 
                sp=await app.download_media(photo.file_id, file_name=f'{app.id}.jpg')
        xp=Image.open(sp)
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(70))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.5)
        Xcen1 = image1.width / 2
        Ycen1 = image1.height / 2
        Xcen2 =xp.width / 2
        Ycen2 = xp.height / 2
        
        #y=changeImageSize(400,400,circle2(youtube,Xcen1,Ycen1))
        y=changeImageSize(400,400,circle(youtube))
        background.paste(y,(690,40),mask=y)
        b=ImageDraw.Draw(background)
        b.pieslice([(690, 40), (1090,440)], 0, 360,outline = "white",width=10)
        x= changeImageSize(270,270,circle(xp))
        background.paste(x, (960,240), mask=x)
        b=ImageDraw.Draw(background)
        b.pieslice([(960,240), (1230,510)], 0, 360,outline ='black',width=10)
    
        draw=ImageDraw.Draw(background)
        font = ImageFont.truetype("assets/TiltWarp-Regular.ttf",35)
        font2 = ImageFont.truetype("assets/FasterOne-Regular.ttf",75)
        arial = ImageFont.truetype("assets/font2.ttf", 30)
        name_font = ImageFont.truetype("assets/font6.ttf", 30)
        font3=ImageFont.truetype("assets/font3.ttf",30)
        font4=ImageFont.truetype("assets/font4.ttf",30)
        font5=ImageFont.truetype("assets/Gugi-Regular.ttf",40)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
                    (30,10),
                    f"{MUSIC_BOT_NAME}",
                    fill="white",
                    stroke_width=5,
                    stroke_fill="black",
                    font=font5,
        )
        draw.text(
                    (100, 100),
                    "NOW PLAYING",
                    fill="white",
                    stroke_width=8,
                    stroke_fill="black",
                    font=font2,
                )
        for line in para:
                    if j == 1:
                        j += 1
                        draw.text(
                            (120, 280),
                            f"{line}",
                            fill="white",
                            stroke_width=5,
                            stroke_fill="black",
                            font=font,
                        )
                    if j == 0:
                        j += 1
                        draw.text(
                            (120, 220),
                            f"{line}",
                            fill="white",
                            stroke_width=5,
                            stroke_fill="black",
                            font=font,
                        )
        draw.text(
                    (120, 340),
                    f"Views : {views[:23]}",
                    (255, 255, 255),
                    font=arial,
                )
        draw.text(
                    (120, 390),
                    f"Duration : {duration[:23]} Mins",
                    (255, 255, 255),
                    font=arial,
                )
        draw.text(
                    (120, 440),
                    f"Channel : {channel}",
                    (255, 255, 255),
                    font=arial,
                )
        
        draw.text(
                (540,550),
                f"ﮩﮩ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ـ٨ـﮩﮩ٨ـﮩ٨ـﮩﮩ٨ـ",
                (255, 255, 255),
                font=name_font,
        )
        draw.text(
            (50, 600),
            f"00:55 ─────────────●─────────────────────────────────────────── {duration}",
            (255, 255, 255),
            font=font3,
        
        )
        draw.text(
                (50,650),
                f"Volume: ■■■■■□□□                      ↻      ◁     II    ▷     ↺",
                (255, 255, 255),
                font=font4,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}_{user_id}.png")
        return f"cache/{videoid}_{user_id}.png"
    except Exception as e:
        return YOUTUBE_IMG_URL

