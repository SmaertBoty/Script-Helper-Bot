import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import re

with open("error_conversions.json","r", encoding="utf-8") as f:
    error_conversions = json.load(f)
    print(error_conversions)

class LogModal(discord.ui.Modal, title="Upload Log"):

    log = discord.ui.TextInput(
        label="Paste your log",
        style=discord.TextStyle.paragraph,
        placeholder="Paste log to redact C:Users/#####/...\n" \
        "If this isn't the main bot, be careful with what you share!",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        content = self.log.value

        anon_log = re.sub(r"(C:[/\\]Users[/\\])[^/\\]+", r"\1#####", content)
    

        await interaction.response.send_message(
            "Redacted Log:\n```\n"+anon_log+"```"
        )
        
class FixModal(discord.ui.Modal, title="Upload Log"):

    log = discord.ui.TextInput(
        label="Paste your log",
        style=discord.TextStyle.paragraph,
        placeholder="Paste your log to get a quick fix.\n" \
        "If this isn't the main bot, be careful with what you share!",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: discord.Interaction):
        content = self.log.value

        for line in content.splitlines():
            for key in error_conversions.keys():
                if key in line:
                    with open("errors/"+error_conversions[key]+".md", "r") as f:
                        await interaction.response.send_message(f.read(), ephemeral=True)
                        return
        
        await interaction.response.send_message("Hmm.. nothing in the common error catologue.", ephemeral=True)

    



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
    await bot.tree.sync()
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
    global topics, error_conversions
    files = os.listdir("topics")
    topics = []
    for topic in files:
        topics.append(topic.removesuffix(".md"))
    
    with open("error_conversions.json","r") as f:
        error_conversions = json.load(f)
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

def find_fix(lines: str):
    for line in lines:
        for key in error_conversions.keys():
            if key in line:
                with open("errors/"+error_conversions[key]+".md","r") as f:
                    
                    return f.read()
    
    return None

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

@bot.tree.command(name="redactlog", description="Redact a log before uploading it.")
async def upload_log(interaction: discord.Interaction):
    await interaction.response.send_modal(LogModal())

@bot.tree.command(name="quickfix", description="Upload a log to get a quick fix suggestion (not shown to others).")
async def anon_fix(interaction: discord.Interaction):
    await interaction.response.send_modal(FixModal())

# Main entry point
if __name__ == "__main__":


    # Run bot
    bot.run(os.getenv("DISCORD_TOKEN"))   