import discord
from discord.ext import commands
import os
from dotenv import load_dotenv




error_conversions = {"return future_value.wait()":"nomappings",
                     "java.lang.ClassNotFoundException:":"nomappings",
                     "error code -1073741515":"nodll",
                     "name 'JavaClass' is not defined":"notpyjinn",
                     "Exited with error code 9009":"nopython",
                     "ModuleNotFoundError: No module named ":"nomodule"}


common_community_modules = ["minescript_plus", "lib_ren", "java", "lib_java"]

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
    
@bot.command(name="quickfix")
async def quickfix(ctx):
    msg = ctx.message
    original_message = None
    
    if msg.reference:
        try: 
            
            original_message = msg.reference.resolved

            if original_message is None:
            
                original_message = await msg.channel.fetch_message(msg.reference.message_id)


        except:
            pass
    
    if original_message is None:
        lines = msg.content.splitlines()
    else:
        lines = original_message.content.splitlines()

    for line in lines:
        for key in error_conversions.keys():
            if key in line:
                with open("errors/"+error_conversions[key]+".md","r") as f:
                    await ctx.send(f.read())
                    return
    
    await ctx.send("Hmm.. nothing in the common error catologue.")
    

# Main entry point
if __name__ == "__main__":


    # Run bot
    bot.run(os.getenv("DISCORD_TOKEN"))   