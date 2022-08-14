from email.mime import application
from http import client
from lib2to3.pgen2 import token
from optparse import Option
import disnake
from disnake import ApplicationCommandInteraction, Embed, Intents
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context


import math 
import asyncio
import random
import os
import sys
import aiosqlite
import json
import typing
from typing import Optional

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


##############
# ECONOMY
############# (not in a cog cos im too tired to mess with that)

@client.event
async def on_ready():
        print("Economy online!")
        client.db = await aiosqlite.connect("bank.db")
        await asyncio.sleep(3)
        async with client.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS bank (wallet INTEGER, bank INTEGER, maxbank INTEGER, user INTEGER)")
        await client.db.commit()
        print("Database ready!")

async def create_balance(user):
        async with client.db.cursor() as cursor:
            await cursor.execute("INSERT INTO bank VALUES(?, ?, ?, ?)", (0,100,500, user.id,))
        await client.db.commit()
        return

async def get_balance(user):
        async with client.db.cursor() as cursor:
            await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id,))
            data = await cursor.fetchone()
            if data is None: 
                await create_balance(user)
                return 0, 100, 500
            wallet, bank, maxbank = data[0], data[1], data[2] 
            return wallet, bank, maxbank

async def update_wallet(user, amount: int):
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT wallet FROM bank WHERE user =?", (user.id,))
        data = await cursor.fetchone()
        if data is None:
            await create_balance(user)
            return 0
        await cursor.execute("UPDATE bank SET wallet = ? WHERE user =?", (data[0] + amount, user.id))
    await client.db.commit()

async def update_bank(user, amount):
    async with client.db.cursor() as cursor:
        await cursor.execute("SELECT wallet, bank, maxbank FROM bank WHERE user = ?", (user.id))
        data = await cursor.fetchone()
        if data is None:
            await create_balance(user)
            return 0
        capacity =int(data[2] - data[1])
        if  amount > capacity:
                await update_wallet(user, amount)
                return 1
        await cursor.execute("UPDATE bank  = ? AND bank = ? WHERE user = ?", (data[0] - amount, data[1] + amount, user.id))
    await client.db.commit()

@client.slash_command(name="balance", description="Check your balance with Raymond")
async def balance (ctx: disnake.CommandInteraction, member: disnake.Member | None = None):
    if member is None:
        member = ctx.author
    wallet, bank, maxbank = await get_balance(member)
    em = disnake.Embed(title=f"{member.name}'s balance")
    em.add_field(name="Wallet", value=wallet)
    em.add_field(name="Bank", value=f"{bank}/{maxbank}")
    await ctx.send(embed=em)

@client.slash_command(name="beg", description="beg for money")
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx: disnake.CommandInteraction):
    chances = random.randint (1, 4)
    if chances == 1:
        return await ctx.send("You got nothing lol")
    amount = random.randint(2, 97)                              # (2 is min, 97 max) you can change however you'd like ;)
    res = await update_wallet(ctx.author, amount)
    if res == 0:
        return await ctx.send("You haven't got an account... dont worry bro i gotchu, try again :)")
    await ctx.send(f"You got {amount} <:acnhbells:1008142980701507725>")    # this emoji won't work for you, change it to coins or another emoji of your choice


@client.slash_command(name="withdraw", description="Withdraw your bells")
@commands.cooldown(1, 5, commands.BucketType.user)
async def withdraw(ctx: disnake.CommandInteraction, amount):
    wallet, bank, maxbank = await get_balance(ctx.author)
    try:
        amount = int(amount)
    except ValueError:
        pass
    if type(amount) == str:
        if amount.lower() == "max" or amount.lower() == "all":
            amount = int(bank)
    else:
        amount = int(amount)

    bank_res = await update_bank(ctx.author, -amount)
    wallet_res = await update_wallet(ctx.author, amount) 
    if bank_res == 0 or wallet_res == 0:
        return await ctx.send("You haven't got an account... dont worry bro i gotchu, try again :)")

    wallet, bank, maxbank = await get_balance(ctx.author)
    em = disnake.Embed(title=f"{amount} <:acnhbells:1008142980701507725> have been withdrawn")
    em.add_field(name="New Wallet", value=wallet)
    em.add_field(name="New Bank", value=f"{bank}/{maxbank}")
    await ctx.send(embed=em)

@client.slash_command(name="deposit", description="deposit your bells")
@commands.cooldown(1, 5, commands.BucketType.user)
async def deposit(ctx: disnake.CommandInteraction, amount):
    wallet, bank, maxbank = await get_balance(ctx.author)
    try:
        amount = int(amount)
    except ValueError:
        pass
    if type(amount) ==str:
        if amount.lower() == "max" or amount.lower() == "all":
            amount = int(wallet)
    else:
        amount = int(amount)

    bank_res = await update_bank(ctx.author, amount)
    wallet_res = await update_wallet(ctx.author, -amount) 
    if bank_res == 0 or wallet_res == 0:
        return await ctx.send("You haven't got an account... dont worry bro i gotchu, try again :)")
    elif bank_res == 1:
        return await ctx.send("You don't have enough storage in your bank *you should probably upgrade sometime...*")

    wallet, bank, maxbank = await get_balance(ctx.author)
    em = disnake.Embed(title=f"{amount} <:acnhbells:1008142980701507725> have been withdrawn")
    em.add_field(name="New Wallet", value=wallet)
    em.add_field(name="New Bank", value=f"{bank}/{maxbank}")
    await ctx.send(embed=em)




client.run("MTAwNDA0Mzc3MjAzNzk3NjA3NA.GaKTjD.GC-4eU1z7yD5y8YQtMBdp_vhPVzjljHaPkoFTk")