import discord
import json
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in!')

prefixDict = {}
try:
    with open('prefixDict.json','r') as f:
        prefixDict = json.load(f)
except FileNotFoundError:
    with open('prefixDict.json','w') as f:
        json.dump(prefixDict, f)

@client.event
async def on_message(message):
    now = datetime.now()
    prefix = ""
    try:
        prefix = prefixDict[message.guild.id]
    except KeyError:
        with open('prefixDict.json','w') as f:
            prefix = "g!"
            prefixDict[message.guild.id] = prefix
            json.dump(prefixDict, f)
# prefix
    if message.content.startswith(prefix + "prefix") and message.author.guild_permissions.manage_messages:
        with open('prefixDict.json','w') as f:
            prefixDict[message.guild.id] = message.content.split()[1]
            json.dump(prefixDict, f)
            await message.channel.send(f"Success! My new prefix is {message.content.split()[1]}")
# ghostPing
    if message.content == prefix + "ghost" or message.content == "<@!BOT ID GOES HERE>":
        await message.channel.send('@everyone')
        f = open("Ghoster_logs.txt", "a")
        f.write("User " + str(message.author.id)
        + " ghostpinged in channel "+ str(message.channel.id)
        + " in server " + str(message.guild.id)
        + " on " + now.strftime("%m/%d/%Y") + " at " + now.strftime("%H:%M:%S")
        + "." + "\n")
        f.close()
        await message.delete()
# message auto-deletion
    if message.content.startswith(prefix + "ghost"):
        with open("Ghoster_logs.txt", "a") as f:
            f.write("User " + str(message.author.id)
            + " deleted " + str(message.content) + "in channel" + str(message.channel.id)
            + " in server " + str(message.guild.id)
            + " on " + now.strftime("%m/%d/%Y") + " at " + now.strftime("%H:%M:%S")
            + "." + "\n")
            f.close()
        await message.delete()
# send message as code block from bot
    if message.content.startswith(prefix + "send "):
        await message.channel.send(f"``` {message.content[6:]} ``` " )
        await message.delete()
# help command
    if message.content == prefix + "help":
        await message.channel.send(f'''
```
Commands:
{prefix}help - displays this message
{prefix}ping - replies Pong.
{prefix}pong - replies Ping. 
{prefix}no - replies OK
{prefix}send - makes the bot send the message in a code block, like this.

```
        ''')
#Fun text commands
    if message.content == prefix + "no":
        await message.channel.send("yes")
    if message.content == prefix + "yes":
        await message.channel.send("no")
    if message.content == prefix + "ping":
        await message.channel.send("`Pong!`")
    if message.content == prefix + "pong":
        await message.channel.send("`Ping!`")

client.run('BOT TOKEN GOES HERE')
