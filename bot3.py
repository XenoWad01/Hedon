import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
from Song import Song
from Queue import Queue

#Config


#   YOUTUBEDL
YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': 'True',
    'default_search': 'auto'
}

#   FFMPEG
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

#Also please make a .env file with your discord token 


# helper function to determine if the bot is connected to a voice channel
def is_connected(context):
    voice_client = get(context.bot.voice_clients, guild=context.guild)
    return voice_client and voice_client.is_connected()


# helper function that plays the next song in the queue
def end_song(guild, voice):
    next_song = queues[guild].cycle_next()
    if queues[guild].isEmpty() and next_song:
        voice.play(FFmpegPCMAudio(next_song.url, **FFMPEG_OPTIONS))
    else:
        print(f'------Queue is not empty we will keep on adding the after lambda song {next_song}')
        voice.play(FFmpegPCMAudio(next_song.url, **FFMPEG_OPTIONS), after=lambda x: end_song(guild, voice))


#load env and declare client as bot with . prefix
load_dotenv()
client = commands.Bot(command_prefix='.')


# this will hold all of the queues (1 per server at a time)
queues = {}


@client.event
async def on_ready():

    print('Bot online')


@client.command()
async def join(context):

    channel = context.message.author.voice.channel
    voice = get(client.voice_clients, guild=context.guild)
    print(f'Connecting to voice channel {voice}')

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    # initiate the queue for this server if it doesent exist
    if not context.guild in queues:
        queues[context.guild] = Queue()

@client.command()
async def godie(context):

    if is_connected(context):

        print('Disconnecting from voice channel.')
        await context.voice_client.disconnect()

    else:

        await context.send("B-bbut I'm already dead :( baka")

@client.command()
async def play(context, text):

    await join(context)
    async with context.typing(): # So bot 'types' while we do heavy stuff 

        #TODO HERE if is_not url get url from text with search then replace text with it and continue
        voice = get(client.voice_clients, guild=context.guild)
        with YoutubeDL(YDL_OPTIONS) as ydl:

            # we first extract the info about the video at url
            info = ydl.extract_info(text, download=False)#, ie_key='YoutubeSearch')

            # we then create a song object with that info and the author of the command
            new_song = Song(info, context.author.nick if context.author.nick else context.author.name)

        # if the queue is empty we play the song otherwise we wait for the queue to naturally populate and depopulate 
        # TODO HERE YOU could add functionality for search so we parse the input into a url
        if queues[context.guild].isEmpty():

            voice.play(FFmpegPCMAudio(new_song.url, **FFMPEG_OPTIONS), after=lambda x: end_song(context.guild, voice))
            voice.is_playing()
            await context.send("*Voice of an angel*")

        else:

            await context.send("*Singing intensifies*")

        # we now add the song that is playing to this server's queue
        queues[context.guild].add(new_song)


@client.command()
async def queue(context):

    await context.send(queues[context.guild])


@client.command()
async def resume(context):

    voice = get(client.voice_clients, guild=context.guild)
    if not voice.is_playing():

        voice.resume()
        await context.send('*Resumes singing*')


@client.command()
async def pause(context):

    voice = get(client.voice_clients, guild=context.guild)
    if voice.is_playing():

        voice.pause()
        await context.send('*Takes a break*')


@client.command()
async def stop(context):

    voice = get(client.voice_clients, guild=context.guild)
    if voice.is_playing():

        voice.stop()
        await context.send('*Quits singing*')


@client.command()
async def clrscr(context, amount=5):

    await context.channel.purge(limit=amount)
    await context.send("Messages have been cleared")


@client.command()
async def playLocalFile(context, text):

    player = FFmpegPCMAudio(text)
    voice = get(client.voice_clients, guild=context.  guild)
    voice.play(player)


@client.command()
async def skip(context):
    voice = get(client.voice_clients, guild=context.guild)
    end_song(context.guild, voice)

client.run(os.getenv('DISCORD_TOKEN'))
