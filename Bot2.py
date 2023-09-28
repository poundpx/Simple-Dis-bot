import os
import discord
import openai
import pytz 
#import datetime
from pytz import timezone
from datetime import datetime,time
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_KEY = os.environ['OPENAI_KEY']

#set up the open API client
openai.api_key = OPENAI_KEY
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

channel = client.get_channel(#ur discord channel)



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  client.loop.create_task(check_time())

  
@client.event
async def on_member_join(member):
  print(f'{member} has joined a server.')


@client.event
async def on_member_remove(member):
  print(f'{member} has lefted a server.')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"{message.content}",
    max_tokens=2048,
    temperature=0.5,
  )
  await message.channel.send(response.choices[0].text)


  
async def check_time():
  global channel 
  channel = client.get_channel(#ur discord channel)
  TIME_ZONE =timezone('US/Eastern')
  NOTIFY_TIME=time(hour=16, minute=46)
  while True:
    now = datetime.now(TIME_ZONE)
    current_time = now.strftime("%H:%M:%S %p")
    current_date = now.strftime("%Y-%m-%d")
    current_T = datetime.strptime(now.strftime("%H:%M"),"%H:%M").time()
   
    if now.weekday()in[1,2] and current_T ==(NOTIFY_TIME):
        await channel.send(f"time {NOTIFY_TIME}")
        await channel.send(f"TIMER{current_T}")
        await channel.send("Hey you going to be late wake up")
        ##await asyncio.sleep(60*60*24)
    await asyncio.sleep(59)

  
client.run(TOKEN)
