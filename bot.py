import discord
from discord.ext import commands

import config
import time
import random

from yt_dlp import YoutubeDL

def get_track_by_name(name):
    YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
	
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with YoutubeDL(YDL_OPTIONS) as ydl:
      track_info = ydl.extract_info(f"ytsearch:{name}", download=False)['entries'][0]
		
      url = track_info['formats'][3]['url']

      return url

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=config.DISCORD_BOT['PREFIX'], intents=intents)

TIME_START = time.time()


# .p <song name> command
bot.remove_command('p')
@bot.command(name='p')
async def p(message, *song):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=message.guild)
        voice.pause()
    except:
        pass

    song = ' '.join(song)

    url = get_track_by_name(song)

    try:
        channel = message.message.author.voice.channel
        voice = discord.utils.get(bot.voice_clients, guild=message.guild)
    except:
        await message.send("вы должны подключиться к голосовому чату")
        return
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice.play(discord.FFmpegPCMAudio(source=url, executable='ffmpeg', before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'), after=lambda e:p(message, *song))
    voice.is_playing()

bot.remove_command('stop')
@bot.command(name='stop')
async def command_handler(message):
    await message.guild.voice_client.disconnect()

    await message.send("пока")


bot.remove_command('uptime')
@bot.command(name='uptime')
async def uptime(message):
    uptime = time.time() - TIME_START

    if uptime > 60 * 60 * 24:
        await message.send(f"uptime: {uptime // (60 * 60 * 24)} days")
    elif uptime > 60 * 60:
        await message.send(f"uptime: {uptime // (60 * 60)} hours")
    elif uptime > 60:
        await message.send(f"uptime: {uptime // 60} minutes")
    else:
        await message.send(f"uptime: {uptime} seconds")


bot.run(config.DISCORD_BOT['TOKEN'])
