import discord
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

prompt_instruction = '''
أنتِ بوت Discord ذكي وذو شخصية خاصة.
تردين على كل شخص حسب أسلوبه:
- إذا كان محترم، تردين بلطف.
- إذا كان ساخر أو وقح، تردين عليه بأسلوب جريء وذكي.
'''

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        user_input = message.content.replace(f"<@{client.user.id}>", "").strip()
        try:
            response = model.generate_content(prompt_instruction + "\n\n" + user_input)
            await message.reply(response.text)
        except Exception as e:
            await message.reply(f"❌ Error: {e}")

client.run(os.getenv("DISCORD_TOKEN"))
