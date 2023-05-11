import discord, os
from keep_alive import keep_alive
import text, media
import sys
from dotenv import dotenv_values
environ = dotenv_values(".env")

async def tombot_msg(message, client):
    if message.author == client.user:
        return
    await text.caller(message)
    await media.caller(message, client)


client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print('{0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await tombot_msg(message, client)


@client.event
async def on_message_edit(msg, message):
    await tombot_msg(message, client)


bot_token = environ['TOKEN']

keep_alive()

client.run(bot_token)
