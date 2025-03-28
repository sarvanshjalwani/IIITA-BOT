import discord
from discord.ext import commands , tasks
from collections import defaultdict
import requests
import time
import os
import json


my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.auto_moderation = True

client = discord.Client(intents=intents)


message_history = defaultdict(list)
SPAM_LIMIT = 5
TIME_WINDOW = 5    

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author.bot:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


  user_id = message.author.id
  now = time.time()
  message_history[user_id].append(now)

  message_history[user_id] = [t for t in message_history[user_id] if (now - t) < TIME_WINDOW]

  if len(message_history[user_id]) > SPAM_LIMIT:
    await message.delete()
    await message.channel.send(f"⚠️ {message.author.mention}, stop spamming!", delete_after=5)
    return

  await client.process_commands(message)


client.run(my_secret)
