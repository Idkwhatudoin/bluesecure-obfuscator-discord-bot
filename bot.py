import io
import os
import subprocess
import discord
import requests
from io import BytesIO
from discord.ext import commands

# fr

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class BetaObfuscateDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Roblox Obfuscator', description='Make sure to enable loadstrings.')
        ]
        super().__init__(placeholder='Select an option', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        subprocess.run(["cmd", "/c", "lua obfuscator.lua"], shell=True)
        with open("output.lua", "rb") as file:
            file_content = file.read()
            await interaction.response.send_message(file=discord.File(fp=BytesIO(file_content), filename="output.lua"))

@bot.command()
async def obfuscate(ctx):
    if ctx.guild is not None:
        embed = discord.Embed(title="This command can only be used over DMs", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if len(ctx.message.attachments) == 0:
        embed = discord.Embed(title="No file attached", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.lua', '.txt')):
        embed = discord.Embed(title="File must be a .lua or .txt file", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    if attachment.size > 20000:
        embed = discord.Embed(title="File size must be 20 KB or less.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    file_content = await attachment.read()
    with open("script.lua", "wb") as file:
        file.write(file_content)

    dropdown = BetaObfuscateDropdown()
    view = discord.ui.View()
    view.add_item(dropdown)
    message = await ctx.send('Select an option', view=view)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(('lua', 'txt')):
        with open("script.lua", "w") as file:
            file.write(message.content)
        
        dropdown = BetaObfuscateDropdown()
        view = discord.ui.View()
        view.add_item(dropdown)
        response = discord.Embed(title="Select an option", color=discord.Color.blurple())
        await message.channel.send(embed=response, view=view)

    await bot.process_commands(message)

bot.run("MTA4MzEwMDkyMTU4NTc0NjAyMA.GS68Q6.PvOyagKrcpjhCXuHvo1j1HvZSVVchkafNOkDW8")
