import os
import sys
from contextlib import closing

import discord
from boto3 import Session
from discord import VoiceClient, Message, Member, VoiceState
from discord.ext import commands
from discord.ext.commands import Context, Cog
import os

from tts.TtsFactory import TtsFactory

BOT_KEY = os.getenv("BOT_KEY")
VOICES = ["Lotte", "Maxim", "Ayanda", "Salli", "Ola", "Arthur", "Tomoko", "Remi", "Geraint", "Miguel", "Giorgio", "Marlene", "Ines", "Kajal", "Zhiyu", "Zeina", "Karl", "Gwyneth", "Joanna", "Lucia", "Cristiano", "Astrid", "Andres", "Vicki", "Mia", "Vitoria", "Bianca", "Chantal", "Raveena", "Daniel", "Amy", "Liam", "Ruth", "Kevin", "Brian", "Russell", "Aria", "Matthew", "Aditi", "Dora", "Enrique", "Hans", "Carmen", "Ivy", "Ewa", "Maja", "Gabrielle", "Nicole", "Filiz", "Camila", "Jacek", "Thiago", "Justin", "Celine", "Kazuha", "Kendra", "Arlet", "Ricardo", "Mads", "Hannah", "Mathieu", "Lea", "Sergio", "Hala", "Tatyana", "Penelope", "Naja", "Olivia", "Ruben", "Laura", "Takumi", "Mizuki", "Carla", "Conchita", "Jan", "Kimberly", "Liv", "Adriano", "Lupe", "Joey", "Pedro", "Seoyeon", "Emma", "Stephen"]

session = Session()
polly = session.client("polly")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

BOT_USER_ID = os.getenv("BOT_USER_ID")
COG_NAME = "GhostOwnerCog"

class GhostOwnerCog(Cog):

    def __init__(self, bot: commands.Bot, owner, voice_client: VoiceClient, speaker: str):
        self.bot = bot
        self.owner = owner
        self.voice_client = voice_client
        self.speaker = speaker
        self.synthesizer = TtsFactory.get_engine("polly")

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.content.startswith("$"):
            return
        if message.author.id == self.owner.id:
            print(f'Message from {message.author}: {message.content}')
            await self.play_message_in_current_channel(message.content)

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.id == self.owner.id:
            if after.channel is None:
                print("Removing Cog!")
                await self.bot.remove_cog(COG_NAME)
            elif before.channel != after.channel:
                print(f"Swapping to channel: {after.channel.name}")
                await self.voice_client.disconnect()
                self.voice_client = await after.channel.connect()


    async def play_message_in_current_channel(self, message_content):
        output = self.synthesizer.get_audio(message_content)
        self.voice_client.play(discord.FFmpegPCMAudio(output))

    async def cog_unload(self) -> None:
        """
        Teardown method
        """
        await self.play_message_in_current_channel("Goodbye!")
        await self.voice_client.disconnect()


@bot.command()
async def join(ctx: Context, speaker):
    if not bot.get_cog(COG_NAME):
        guild = bot.get_guild(ctx.author.mutual_guilds[0].id)
        member = guild.get_member(ctx.author.id)
        await guild.me.edit(nick=ctx.author.display_name + "-ghost")
        vc = await member.voice.channel.connect()
        speaker = speaker.split(" ")[0].capitalize()

        if not speaker or speaker not in VOICES:
            speaker = "Matthew"

        await bot.add_cog(GhostOwnerCog(bot, ctx.author, vc, speaker))
    else:
        await ctx.send("I'm already in a channel!")


@bot.command()
async def leave(ctx):
    cog = bot.get_cog(COG_NAME)
    if cog:
        guild = bot.get_guild(ctx.author.mutual_guilds[0].id)
        await guild.me.edit(nick="The Medium")
        await bot.remove_cog(COG_NAME)
    else:
        await ctx.send("I'm not currently in a channel!")

@bot.command()
async def speakers(ctx):
    await ctx.send(", ".join(VOICES))

bot.run(BOT_KEY)


