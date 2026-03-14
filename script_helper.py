import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


files = os.listdir("topics")
topics = []
for topic in files:
    topics.append(topic.removesuffix(".md"))


# Load environment variables
load_dotenv()

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content
intents.members = True          # Required for member-related events

# Initialize bot
bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is online and ready!")
    await bot.change_presence(activity=discord.Game("with you!"))

# Example command
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="t")
async def topic(ctx, page):
    req = page.lower()
    if req in topics:
        with open("topics/"+req+".md","r") as f:
            await ctx.send(f.read())
    else:
        await ctx.message.add_reaction("❌")

@bot.command(name="refresh")
async def refresh(ctx):
    global topics
    files = os.listdir("topics")
    topics = []
    for topic in files:
        topics.append(topic.removesuffix(".md"))
    await ctx.message.add_reaction("🔄")
    
@bot.command(name="format")
async def format(ctx):
    msg = ctx.message
    if msg.reference:
        try:
             # Try to use the cached message first
            original_message = msg.reference.resolved 
            if original_message is None:
                # If not in cache, fetch the message from the API
                original_message = await msg.channel.fetch_message(msg.reference.message_id)
            await msg.channel.send("```python\n"+original_message.content+"```")
        except:
            pass
    else:
        await ctx.send("Respond to a message to use this command.")
    

# Main entry point
if __name__ == "__main__":


    # Run bot
    bot.run(os.getenv("DISCORD_TOKEN"))   