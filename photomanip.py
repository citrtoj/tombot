import os
import requests
from PIL import Image
import urllib.request
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def find_img_attachments(message):
    attachments = message.attachments
    for attachment in attachments:
        if 'image' in attachment.content_type:
            return attachment.url
    if message.embeds:
        for embed in message.embeds:
            return (embed.image.url)


def greenscreen(img):
    img = img.convert("RGBA")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = img.getpixel((x, y))
            if (r > 0) and (r < 127) and (g >= 87) and (b <= 120):
                pixdata[x, y] = (255, 255, 255, 0)
            #remove anti-aliasing outline of body
            if a < 100:
                pixdata[x, y] = (255, 255, 255, 0)
    return img


def urlimg(link):
    #TODO: cred ca cateodata filename imi da null
    #ar trb sa modific
    filename = link.split('/')[-1]
    urllib.request.urlretrieve(link, filename)
    return filename


def reqimg(link):
    #imgflip doesnt like urlretrieve
    filename = "ifljpg.jpg"
    req = requests.get(link, allow_redirects=True)
    open(filename, 'wb').write(req.content)
    return filename


def reqbg(link):
    #apparently some links dont like urlretrieve either
    #so i made this separate fxn for the bg
    #so that i could have custom filenames and all
    filename = link.split('/')[-1]
    req = requests.get(link, allow_redirects=True)
    open(filename, 'wb').write(req.content)
    return filename


def crop_image(imageobj):
    #this one's for the bg, so that it fits to the
    #1280x720 of the tom template
    image = imageobj
    width, height = image.size
    w = 1280
    h = 720
    target_aspect = float(16 / 9)
    image_aspect = float(width / height)

    if image_aspect < target_aspect:
        hgt = int(height * w / width)
        image = image.resize((w, hgt))

    #for aspect ratio smaller than 16 by 9
    else:
        wdt = int(width * h / height)
        image = image.resize((wdt, h))
    width, height = image.size
    left = int((width - w) / 2)
    top = int((height - h) / 2)
    right = left + w
    bottom = top + h
    image = image.crop((left, top, right, bottom))
    return image


def toSvg(filename):
    drawing = svg2rlg(filename)
    newfile = "svg" + ".png"
    renderPM.drawToFile(drawing, newfile, fmt='PNG')
    return newfile


def toPng(filename):
    try:
        if filename.split('.')[-1] == "svg":
            filename = toSvg(filename)
            return filename
        else:
            with Image.open(filename) as img:
                newfile = filename.split('.')[-1] + ".png"
                img.save(newfile, "PNG")
            os.remove(filename)
            return newfile
    except:
        print("toPng: Failed during PNG process")


def superimpose(tompng, bgjpg):
    try:
        bg = Image.open(bgjpg)
        png = Image.open(tompng)
        print("Superimpose: Opened images")
    except:
        print("Superimpose: Opening images failed.")
    else:
        try:
            bg = crop_image(bg).convert('RGBA')
            print("Superimpose: Cropped background")
        except:
            print("Superimpose: Cropping bg failed")
        else:
            try:
                png = greenscreen(png)
                print("Superimpose: greenscreened Imgflip image")
            except:
                print("Superimpose: greenscreening Imgflip image failed")
            else:
                try:
                    png = png.resize((1280, 720))
                    print("Superimpose: resized PNG")
                except:
                    print("Superimpose: resizing PNG failed")
                else:
                    try:
                        bg.paste(png, (0, 0), png)
                        print("Superimpose: pasted PNG on top")
                    except:
                        print("Superimpose: pasting failed")
                    else:
                        try:
                            bg.save('iamatfinal.png', 'PNG')
                            return "iamatfinal.png"
                        except:
                            print("Superimpose: saving failed")
