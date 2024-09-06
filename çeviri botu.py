import discord
from discord.ext import commands, tasks
from itertools import cycle
from langdetect import detect
from deepl import Translator
import os

intents = discord.Intents.all()
translator = Translator("your-key-here")  # Replace with your actual DeepL API key
bot = commands.Bot(command_prefix="/", intents=intents)

# List of statuses to cycle through
status_list = cycle([
    discord.Game("Translating messages"),
    discord.Game("Helping users"),
    discord.Game("Available for commands"),
    discord.Game("Working hard"),
])

@bot.event
async def on_ready():
    change_status.start()  # Start the status rotation task
    print(f'{bot.user} has connected to Discord!')

@tasks.loop(seconds=30)  # Change status every 30 seconds
async def change_status():
    await bot.change_presence(activity=next(status_list))

@bot.event
async def on_message(message):
    if message.author == bot.user:  # Ignore bot's own messages
        return
    if message.author.bot:  # Ignore messages from other bots
        return
    try:
        source_lang = detect(message.content)
        if source_lang == "tr":  # If the message is in Turkish, no translation is needed
            return  
        result = translator.translate_text(message.content, target_lang="TR")
        await message.channel.send(f'Translated to Turkish: {result.text}')
    except Exception as e:
        await message.channel.send(f'Error: {str(e)}')

bot.run('your-token-here')  # Replace 'YOUR_BOT_TOKEN' with your bot's token