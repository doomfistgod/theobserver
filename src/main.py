import os
import discord
import openai
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

openai.api_key = os.getenv('API_KEY')
token = os.getenv('TOKEN')
channel_id = (os.getenv('channel_id'))
mohammed = (os.getenv('mohammed_id'))
faisal = (os.getenv('faisal_id'))
model_id = 'gpt-3.5-turbo'






intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

faisal_logs = []
mohammed_logs = []


@client.event
async def on_ready():
  print(f'Logged in as {client.user}')


@client.event
async def on_presence_update(before, after):
  global faisal_logs, mohammed_logs
  user_id = None
  logs = None

  if after.id == faisal:
    user_id = faisal
    logs = faisal_logs
  elif after.id == mohammed:
    user_id = mohammed
    logs = mohammed_logs

  if user_id is None or logs is None:
    return

  overwatch = ['Overwatch 2']
  if after.activity and after.activity.name not in overwatch:
    if before.activity or after.activity in logs:
      return
    logs.append(after.activity.name)

    channel = client.get_channel(channel_id)
    await channel.send(f"<@{user_id}> باع القضية للمرة {len(logs)}")

  elif after.activity and after.activity.name in overwatch:
    if before.activity or after.activity in logs:
      return

    logs.clear()
    completion_pos = openai.ChatCompletion.create(
      model=model_id,
      messages=[{
        "role":
        "user",
        "content":
        f"write a sophisticated 5 lines of poetry about this person's <@{user_id}> valor and courage , and at the end thank him for playing the game overwatch. you must mention the following name <@{user_id}> in the poem"
      }])
    reply_content_pos = completion_pos.choices[0].message.content
    channel = client.get_channel(channel_id)
    await channel.send(reply_content_pos)


client.run(token)
