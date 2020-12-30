# bot.py
import os

import discord
import requests
import dotenv
import pickle5 as pickle
from dotenv import load_dotenv
from discord.ext import tasks
from itertools import cycle

from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISC_TOKEN')
GUILD = os.getenv('DISC_GUILD')

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

respdict = {}
respdict = load_obj('resppair')

pointdict = {150685106074419201:0}
save_obj(pointdict,'pointdict')
pointdict = load_obj('pointdict')

app = Flask('')

@app.route('/')
def main():
  return "Your Flask Is Ready"

def run():
  app.run(host='0.0.0.0', port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('hello'):
        await message.channel.send('Hello')

    if message.content.startswith('/s'):
        string = message.content
        tosend = ""
        ctr = 0
        for i in string:
            ctr += 1
            if ctr > 2:
                if ctr % 2 == 0:
                    tosend += i.upper()
                else:
                    tosend += i.lower()
        tonick = message.author.display_name
        await message.guild.me.edit(nick=tonick)
        await message.channel.send(tosend)
        await message.guild.me.edit(nick="LawrenceBot")
        await message.delete()

    if message.content == ('deleteme'):
        await message.delete()

    if message.content == ('ur mom'):
        await message.channel.send('is beautiful')

    if message.content.startswith('!pairadd'):
        response = ""
        stimulus = ""
        flag = 0
        for i in message.content[8:]:
            if i == '>':
                flag = 1
            else:
                if flag == 1:
                    response += i
                else:
                    stimulus += i
        if flag == 0:
          await message.channel.send('Syntax bad')
        else:
          response = response.strip()
          stimulus = stimulus.strip()
          respdict[stimulus] = response
          save_obj(respdict, 'resppair')
          await message.channel.send('Accepted')

    if message.content in respdict :
      await message.channel.send(respdict[message.content])

    if message.content.startswith('1pt'):
      await message.channel.send('Tag who you want to give a point to')
      msg = await client.wait_for('message', check=check, timeout=30)
      if not msg.mentions:
          await msg.channel.send('Tag not found, point cancelled')
      else:
          if msg.mentions[0].id == message.author.id:
              await msg.channel.send('https://tenor.com/view/oozora-subaru-vtuber-hololive-cute-anime-gif-17369692')
          else:
            if msg.mentions[0].id in pointdict:
              pointdict[msg.mentions[0].id] += 1
              await msg.channel.send(f'Point given to {msg.mentions[0]}')
            else:
              pointdict[msg.mentions[0].id] = 1
              await msg.channel.send(f'First point given to {msg.mentions[0]}')
            save_obj(pointdict,'pointdict')

    if message.content.startswith('!points'):
      for key in pointdict:
        name = message.guild.get_member(key).name
        await message.channel.send(f'{name}:{pointdict[key]}')

    if message.content.startswith('!clearpoints'):
      for key in pointdict:
        pointdict[key]=0
      save_obj(pointdict,'pointdict')

def check(message):
    return True


status = cycle(['with Desmos', 'Minecraft'])


@client.event
async def on_ready():
    change_status.start()
    keep_alive()
    print("Your bot is ready")

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run(TOKEN)
