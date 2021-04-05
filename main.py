import discord
import json
import asyncio
import os
import math
import random
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
from itertools import cycle
from async_timeout import timeout
from discord.ext import commands
from keep_alive import keep_alive
import discord
from pretty_help import PrettyHelp, Navigation
from random import choice
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system
from termcolor import colored, cprint
from pytz import timezone
import discord
import configparser
import praw
import urllib3
import time
import datetime
import sys
import shutil
import functools


bot = commands.Bot(command_prefix="+")
status = cycle(['Meow', 'Listening to Unravel - Tokyo Ghoul'])


@bot.event
async def on_ready():
  print('Bot is ready.')

@bot.event
async def on_member_join(member):
  role = discord.utils.get(member.server.roles, name='Member')
  await client.add_roles(member, role)

@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_member_join(member):
  print(f'{member} has joined a server.')

@bot.event
async def on_member_remove(member):
  print(f'{member} has left a server.')

@bot.command()
async def test(ctx):
  await ctx.send("test")

@bot.command()
async def clear(ctx, amount=10000000000000000000000000000000000000000000000000000):
  await ctx.channel.purge(limit=amount)


@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send('Kicked User!')

@bot.command(pass_content=True)
async def join (ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("left voice channel")


@bot.command(description="bans a user with specific reason (only admins)") #ban
@commands.has_permissions(administrator=True)
async def ban (ctx, member:discord.User=None, reason =None):
 try:
    if (reason == None):
        await ctx.channel.send("You  have to specify a reason!")
        return
    if (member == ctx.message.author or member == None):
        await ctx.send("""You cannot ban yourself!""") 
    else:
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(message)
        await ctx.guild.ban(member, reason=reason)
        print(member)
        print(reason)
        await ctx.channel.send(f"{member} is banned!")
 except:
    await ctx.send(f"Error banning user {member} (cannot ban owner or bot)")

@bot.command(description="Unbans ppl who have been banned")
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member: discord.Member):
    await ctx.guild.unban(member)

@bot.command(description="Just okay?")
async def Okay(ctx):
  await ctx.send("Okay? Do you need help with anything. If so use the 'help' command")

@bot.command(description="Use Hello for just saying hi!")
async def Hello(ctx):
  await ctx.send("Hi! How r u!")


# custom ending note using the command context and help command formatters
ending_note = "The ending not from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

# ":discord:743511195197374563" is a custom discord emoji format. Adjust to match your own custom emoji.
nav = Navigation(":discord:743511195197374563", "👎", "\U0001F44D")
color = discord.Color.dark_gold()

bot.help_command = PrettyHelp(navigation=nav, color=color, active_time=5, ending_note=ending_note)

keep_alive() 
bot.run('<Your token here>')
