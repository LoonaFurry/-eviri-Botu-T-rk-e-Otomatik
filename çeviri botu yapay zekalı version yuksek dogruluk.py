import discord
from discord.ext import commands
import google.generativeai as genai

# Configure the Gemini API with your API key
genai.configure(api_key="your-api-key")


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Function to detect language using Gemini API
def detect_language_with_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Prompt clearly asks Gemini to identify the language of the given text
        prompt = f"Identify the language of the following text and respond with the language code (e.g., 'en' for English, 'fr' for French, 'tr' for Turkish):\n\n{text}"
        response = model.generate_content(prompt)
        detected_language = response.text.strip().lower()
        return detected_language
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

# Function to translate text using Gemini API
def translate_with_gemini(text, target_lang="TR"):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Prompt instructs Gemini to translate the text into the specified target language
        prompt = f"Translate the following text to {target_lang}:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()  # Ensure leading/trailing whitespace is removed
    except Exception as e:
        print(f"Translation error: {e}")
        return None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    try:
        # Detect the language of the message using Gemini
        source_lang = detect_language_with_gemini(message.content)
        target_lang = "tr"  # Set target language to Turkish (use lowercase for language codes)

        # Skip translation if the source language is the same as the target language
        if source_lang and source_lang == target_lang:
            return

        translated_text = translate_with_gemini(message.content, target_lang)
        if translated_text:  # Only send non-empty translations
            await message.channel.send(f'Translated to Turkish: {translated_text}')
    
    except Exception as e:
        await message.channel.send(f'Error: {e}')

bot.run('your-token-here')  # Replace 'YOUR_BOT_TOKEN' with your bot's token