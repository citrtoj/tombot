import discord, os, re, requests, json, random
import photomanip as imat

from dotenv import dotenv_values
environ = dotenv_values(".env")

#"Tombot show me a [prompt] gif"
async def show_gif(message):
    gifregex = re.search(r'\b(?:(tombot show me a)(n?)\s)(.*?)(?: gif)\b',
                         message.content,
                         flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
    if gifregex:
        gifsearch = gifregex.group(3)
        if gifsearch:
            tenorkey = environ['tenorkey']
            giflimit = 12
            r = requests.get(
                "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" %
                (gifsearch, tenorkey, giflimit))
            if r.status_code == 200:
                gifjson = json.loads(r.content)
                rand = random.randint(
                    0, min(giflimit - 1,
                           len(gifjson["results"]) - 1))
                sendgif = gifjson["results"][rand]["itemurl"]
                await message.channel.send(sendgif)
            else:
                await message.channel.send("Couldn't find any " + gifsearch +
                                           " gif, sorry.")
    else:
        return


#"Tombot I am [preposition] [prompt]"
prepositions = [
    "on the edge of", "under", "on top of", "behind", "in front of", "under",
    "over", "inside", "in", "outside of", "outside", "across from", "next to",
    "near", "on", "at", "up"
]
regex = r"\b(tombot)[,.?!]*? (((i am|i'm) *(" + '|'.join(
    prepositions) + r"))( *)(.*?)\b$)"


async def i_am_at(message, client):
    if re.search(regex,
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        loc = re.search(regex,
                        message.content,
                        flags=re.IGNORECASE | re.MULTILINE
                        | re.UNICODE).group(7)
        toptext = re.search(regex,
                            message.content,
                            flags=re.IGNORECASE | re.MULTILINE
                            | re.UNICODE).group(3)
    else:
        loc = 0
    iflpw = environ['imgflipkey']
    if loc != 0:
        replied_to = None
        if message.reference is not None:
            replied_to = await message.channel.fetch_message(
                message.reference.message_id)
        iflTemplate = "343044476"
        if replied_to != None:
            if replied_to.author == client.user and replied_to.attachments is not None and imat.find_img_attachments(
                    replied_to).split('/')[-1] == "iamatfinal.png":
                iflTemplate = "362586438"
        await message.channel.send("*Travelling to " + loc + "...*")
        r = requests.get(
            "https://api.imgflip.com/caption_image?template_id=%s&username=%s&password=%s&text0=%s&text1=%s"
            % (iflTemplate, 'mackiespizzas', iflpw, toptext, loc))
        if r.status_code == 200:
            ifljson = json.loads(r.content)
            ifljpg = ifljson["data"]["url"]
            attachlink = None
            if message.reference is None:
                if message.attachments is None:
                    attachlink = None
                else:
                    attachlink = imat.find_img_attachments(message)
            else:
                attachlink = imat.find_img_attachments(replied_to)
            if attachlink is not None:
                attachimg = imat.toPng(imat.reqbg(attachlink))

                tomjpg = imat.reqimg(ifljpg)
                final = imat.superimpose(tomjpg, attachimg)
                if final:
                    await message.channel.send(file=discord.File(final))
                else:
                    await message.channel.send("Couldn't get there, sorry.")
                os.remove(attachimg)
                os.remove(tomjpg)
                os.remove(final)

            else:
                search_query = loc.replace('#', ' ')
                url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

                querystring = {
                    "q": search_query,
                    "pageNumber": "1",
                    "pageSize": "10",
                    "autoCorrect": "true"
                }

                headers = {
                    "X-RapidAPI-Key":
                    environ["rapidapikey"],
                    "X-RapidAPI-Host":
                    "contextualwebsearch-websearch-v1.p.rapidapi.com"
                }

                bingimg = requests.request("GET",
                                           url,
                                           headers=headers,
                                           params=querystring)
                if bingimg.status_code == 200:
                    bingjson = json.loads(bingimg.content)
                    if len(bingjson["value"]) > 0 and "error" not in bingjson:
                        try:
                            bingresult = bingjson["value"][random.randint(
                                0, min(len(bingjson["value"]), 4))]["url"]
                            bingjpg = imat.reqbg(bingresult)
                            tomjpg = imat.reqimg(ifljpg)
                            if (bingjpg[-3:] != "png"):
                                bingjpg = imat.toPng(bingjpg)
                            final = imat.superimpose(tomjpg, bingjpg)
                            if final:
                                await message.channel.send(
                                    file=discord.File(final))
                            else:
                                await message.channel.send(
                                    "Couldn't get there, sorry... (Final image invalid)"
                                )
                            os.remove(bingjpg)
                            os.remove(tomjpg)
                            os.remove(final)
                        except:
                            await message.channel.send(
                                "Couldn't get there, sorry... (Failed somewhere during the superimposing process)"
                            )
                            return
                    else:
                        await message.channel.send(
                            "Couldn't get there, sorry... (Image API returned either 0 images or an error)"
                        )
                else:
                    await message.channel.send(
                        "Couldn't get there, sorry... (Image API GET request unsuccessful)"
                    )
        else:
            await message.channel.send(
                "Couldn't get there, sorry... (Imgflip status code != 200)")
    else:
        return


async def caller(message, client):
    await show_gif(message)
    await i_am_at(message, client)
