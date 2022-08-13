from email.mime import application
from http import client
from lib2to3.pgen2 import token
from optparse import Option
import disnake
from disnake import ApplicationCommandInteraction, Embed, Intents
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

tree = app_com


import math 
import random
import os
import sys

Intents.send_messages = True
disnake.ext.commands.when_mentioned 



client= commands.Bot(command_prefix="r!")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.slash_command(name="ping", description="wonder what this does...")
async def cmd1(ctx):
    await ctx.send("pong :ping_pong:", ephemeral=True)

@client.slash_command(name="raymaid", description="surprisngly good femboy")
async def cmd2(ctx):
    await ctx.send("https://media.discordapp.net/attachments/1004047029544177775/1004066623159812116/raymaid.png?width=556&height=671", ephemeral=False)

@client.slash_command(name="application", description="to become a helper")
async def cmd3(ctx):
    await ctx.send("Applications right now are closed!", ephemeral=True)

@client.slash_command(name="jobwarn", description="warns you about job")
async def cmd4(ctx):
    await ctx.send("Remember that everything in this server is free, if someone insists you pay them please contact staff immediately.", ephemeral=True)






client.run("TOKEN")