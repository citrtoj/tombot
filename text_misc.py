#text-related functions that are small or do not require an external API besides discord

import re, random, discord
import eng_to_ipa as ipa


#for singing Country Roads along with Tombot, for whatever reason
async def roads(message):
    prompts = {
        r'\b(\d*?(country)[,.]*? *(roads)[,.]*?\d*?$)':
        "Take me home.",
        r'\b(\d*?(to)[,.]*? *(the)[,.]*? *(place)[,.]*?\d*?$)':
        "I belong.",
        r'\b(\d*?(west)[,.]*? *(virginia)\d*?$)':
        "Mountain mama.",
        r'\b(\d*?(take)[,.]*? *(me)[,.]*? *(home)[,.]*?\d*?$)':
        "Country roads.",
        r'\b(\d*?(country)[,.]*? *(roads)[,.]*? *(take)[,.]*? *(me)[,.]*? *(home)[,.]*?\d*?$)':
        "To the place I belong.",
        r'\b(\d*?(almost)[,.]*? *(heaven)[,.]*?\d*?$)':
        "West Virginia.",
        r'\b(\d*?(blue)[,.]*? *(ridge)[,.]*? *(mountains)[,.]*?\d*?$)':
        "Shenandoah River.",
        r'\b(\d*?(life)[,.]*? *(is)[,.]*? *(old)[,.]*? *(there)[,.]*?\d*?$)':
        "Older than the trees.",
        r'\b(\d*?(younger)[,.]*? *(than)[,.]*? *(the)[,.]*? *(mountains)[,.]*?\d*?$)':
        "Blowin' like a breeze."
    }
    for prompt in prompts:
        countryRoads = re.search(prompt,
                                 message.content,
                                 flags=re.IGNORECASE | re.UNICODE)
        if countryRoads:
            if countryRoads.group(1) == message.content:
                await message.channel.send(prompts[prompt])


#"Thanks, Tombot"
async def thanks(message):
    if re.search(r'\b(thanks)[ ,.?!]*?(tombot)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE) or re.search(
                     r'\b(tombot)[,.? !]*?(thanks)\b',
                     message.content,
                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        await message.channel.send("You're welcome!")


#"Tombot, IPA this"
async def read(message):
    if re.search(r'\b(tombot).*?(IPA this)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        if message.reference is not None:
            msg = await message.channel.fetch_message(
                message.reference.message_id)
            msgcnt = msg.content
            await message.channel.send(ipa.convert(msgcnt))


#"Tombot, choose between [options...]"
async def choose(message):
    choose = re.search(r'\b(?:(tombot[,. ]*?choose( between)?)\s*)(.*)',
                       message.content,
                       flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
    if choose:
        choose_list = choose.group(3)
        list_items = re.split(',', choose_list)
        while ("" in list_items):
            list_items.remove("")
        for item in list_items:
            item.strip()
        rand = random.randint(0, len(list_items) - 1)
        await message.channel.send(list_items[rand])


async def echo(message):
    echo = re.search(r'\b^(?:(tombot[,. ]*?echo)\s*)(.*)',
                     message.content,
                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
    if echo:
        prompt = echo.group(2)
        if prompt:
            await message.channel.send(prompt)
            try:
                await message.delete()
            except Exception as e:
                print("Unable to delete message: " + e)


async def help(message):
    if re.search(r'\b(tombot).*?(what can you do)\b',
                 message.content,
                 flags=re.IGNORECASE | re.MULTILINE | re.UNICODE) or re.search(
                     r'\b(tombot).*?(help)\b',
                     message.content,
                     flags=re.IGNORECASE | re.MULTILINE | re.UNICODE):
        await message.channel.send(
            """Hello! I'm Tombot, and here's a list of some things you can ask me right now (replace "<prompt>" with whatever you wish):
            
- "Tombot, what can you do?" / "Tombot, help"
- "Tombot, show me a/an <prompt> gif"
- "Tombot, I am at <prompt>" (other prepositions such as "in", "on", "under", "inside", etc. are also supported)
- (in reply to a message with image) "Tombot, read this"
- (in reply to a message with text) "Tombot, translate this"
- "Country roads"
- "Tombot, echo <prompt>"
- "Tombot, choose between <multiple prompts, separated by commas>"
- "Tombot, define <prompt> / Tombot, what does <prompt> mean?"

This list is not exhaustive and some of the commands might behave intentionally differently in some situations, but I couldn't be arsed to write them all here. You're probably going to discover them as you go anyway. Have fun!
        """)


async def caller(message):
    await roads(message)
    await thanks(message)
    await read(message)
    await choose(message)
    await echo(message)
    await help(message)