import discord, os, json, requests, re, textwrap, photomanip, string
import text_misc as misc
import urllib.parse
import html

from dotenv import dotenv_values
environ = dotenv_values(".env")

#"Tombot, convert this"
def convert_temps_util(val, unit):
    val = float(val)
    if unit == "c":
        val = 9 * val / 5 + 32
        unit = "f"
    elif unit == "f":
        val = (val - 32) * 5 / 9
        unit = "c"
    temp = str(round(val, 2)) + '°' + unit.upper() + '\n'
    return temp


async def convert_temps(message):
    if re.search(r'\b(tombot).*?(convert this)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        if message.reference is not None:
            msg = await message.channel.fetch_message(
                message.reference.message_id)
            temps = re.findall(r'\b(\-?[0-9]+.?[0-9]*)\s*?°?\s*?([CFK])\b',
                               msg.content,
                               flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
            if temps:
                temps_list = ""
                for temp in temps:
                    temp_val = temp[0]
                    temp_unit = temp[1].lower()
                    temps_list += convert_temps_util(temp_val, temp_unit)
                await message.channel.send(temps_list)


async def convert_currency(message):
    #soon
    if re.search(r'\b(tombot).*?(convert this)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        if message.reference is not None:
            msg = await message.channel.fetch_message(
                message.reference.message_id)
            temps = re.findall(r'\b(\-?[0-9]+.?[0-9]*)\s*?°?\s*?([CFK])\b',
                               msg.content,
                               flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
            if temps:
                temps_list = ""
                for temp in temps:
                    temp_val = temp[0]
                    temp_unit = temp[1].lower()
                    temps_list += convert_temps_util(temp_val, temp_unit)
                await message.channel.send(temps_list)

#[in reply to an image] "Tombot, read this"
async def ocr(message):
    if re.search(r'\b(tombot).*?(read this)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        msgimg = ""
        if message.reference is not None:
            msg = await message.channel.fetch_message(
                message.reference.message_id)
            msgimg = photomanip.find_img_attachments(msg)
        else:
            msgimg = photomanip.find_img_attachments(message)
        if msgimg == "":
            await message.channel.send("There's no image to read.")
        url = 'https://api.ocr.space/parse/imageurl?apikey={0}&url={1}&isOverlayRequired=false'.format(
            environ['ocrspacekey'], msgimg)
        payload = {}
        headers = {'apikey': environ['ocrspacekey']}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            ocrjson = json.loads(response.text)
            if ocrjson['OCRExitCode'] == 3:
                await message.channel.send(
                    "The image is bigger than 1024KB. I can't read it. Sorry.")
            else:
                if ocrjson['OCRExitCode'] == 1:
                    ocrtext = ocrjson['ParsedResults'][0]['ParsedText']
                    if ocrtext:
                        if len(ocrtext) > 2000:
                            lines = textwrap.wrap(ocrtext,
                                                  2000,
                                                  break_long_words=False)
                            for line in lines:
                                await message.channel.send(line)
                        else:
                            await message.channel.send(ocrtext)
                        if (await misc.pee_util(ocrtext)):
                            await misc.pee(message, 1)
                        penis_words = re.search(r'\b\d*?(penis)\d*?\b',
                                                ocrtext,
                                                flags=re.IGNORECASE
                                                | re.MULTILINE | re.UNICODE)
                        if penis_words:
                            await message.channel.send(
                                file=discord.File('media/penis.png'))
                    else:
                        await message.channel.send(
                            "I can't see any text in the image.")
        else:
            await message.channel.send("I have no idea why, but I can't.")


#"Tombot, translate this" / "Tombot, tradu asta"
async def translate(message):
    if re.search(r'\b(tombot).*?(translate this)|(tradu asta)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        if message.reference is not None:
            msg = await message.channel.fetch_message(
                message.reference.message_id)
            msgcnt = msg.content

            import requests

            url = "https://google-translator9.p.rapidapi.com/v2"
            target = "en"
            isTarget = re.search(r'(to )(([^\b ]){2}\b)',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
            if isTarget:
              target = isTarget.group(2)
            payload = {
            	"q": msgcnt,
            	"target": target,
            	"format": "text"
            }
            headers = {
            	"content-type": "application/json",
            	"X-RapidAPI-Key": environ['rapidapikey'],
            	"X-RapidAPI-Host": "google-translator9.p.rapidapi.com"
            }
            
            response = requests.request("POST", url, json=payload, headers=headers)
            
            response = response.json()['data']['translations'][0]['translatedText']
            await message.channel.send(response)


#"Tombot, define [prompt]" / "Tombot, what does [prompt] mean?"
async def definition(message):
    whats = re.search(
        r'\b(?:(tombot,?.*? what does)(n?)\s*)"?(.*?)"?(?: mean\??)',
        message.content,
        flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
    define = re.search(r'\b(?:(tombot[,. ]*?define)\s*)(.*)',
                       message.content,
                       flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
    if whats or define:
        if whats:
            term = whats.group(3)
        if define:
            term = define.group(2)
            term = term.translate(str.maketrans('', '', string.punctuation))
        dict = requests.get(
            "https://api.dictionaryapi.dev/api/v2/entries/en/" + term)
        msg = '"' + term + '" means:\n'
        if dict.status_code == 200:
            if True:
                dictjson = json.loads(dict.content)
                for index, meaning in enumerate(dictjson[0]["meanings"]):
                    msg = msg + str(
                        index + 1) + ". **" + meaning["partOfSpeech"] + "**:\n"
                    for defi in meaning["definitions"]:
                        msg = msg + "- " + defi["definition"] + "\n"
                await message.channel.send(msg)
        else:
            await message.channel.send(file=discord.File('media/dont_know.mp4')
                                       )


async def caller(message):
    await convert_temps(message)
    await ocr(message)
    await translate(message)
    await definition(message)
    #await echo(message)
    await misc.caller(message)
