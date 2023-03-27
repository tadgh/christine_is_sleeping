import logging

import discord
from boto3 import Session
from discord import VoiceClient, Message, Member, VoiceState
from discord.ext import commands
from discord.ext.commands import Context, Cog
import os

from dotenv import load_dotenv

from tts.TtsFactory import TtsFactory
load_dotenv()

BOT_KEY = os.getenv("BOT_KEY")
VOICES = ["Lotte", "Maxim", "Ayanda", "Salli", "Ola", "Arthur", "Tomoko", "Remi", "Geraint", "Miguel", "Giorgio", "Marlene", "Ines", "Kajal", "Zhiyu", "Zeina", "Karl", "Gwyneth", "Joanna", "Lucia", "Cristiano", "Astrid", "Andres", "Vicki", "Mia", "Vitoria", "Bianca", "Chantal", "Raveena", "Daniel", "Amy", "Liam", "Ruth", "Kevin", "Brian", "Russell", "Aria", "Matthew", "Aditi", "Dora", "Enrique", "Hans", "Carmen", "Ivy", "Ewa", "Maja", "Gabrielle", "Nicole", "Filiz", "Camila", "Jacek", "Thiago", "Justin", "Celine", "Kazuha", "Kendra", "Arlet", "Ricardo", "Mads", "Hannah", "Mathieu", "Lea", "Sergio", "Hala", "Tatyana", "Penelope", "Naja", "Olivia", "Ruben", "Laura", "Takumi", "Mizuki", "Carla", "Conchita", "Jan", "Kimberly", "Liv", "Adriano", "Lupe", "Joey", "Pedro", "Seoyeon", "Emma", "Stephen"]
ENGINES = ["elevenlabs", "polly"]

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = False



bot = commands.Bot(command_prefix='$', intents=intents)

BOT_USER_ID = os.getenv("BOT_USER_ID")
COG_NAME = "GhostOwnerCog"

class GhostOwnerCog(Cog):

    def __init__(self, bot: commands.Bot, owner, voice_client: VoiceClient, engine: str,  speaker: str):
        self.bot = bot
        self.owner = owner
        self.voice_client = voice_client
        self.speaker = speaker
        self.synthesizer = TtsFactory.get_engine(engine, speaker)
        print(f"Joined {voice_client.channel.name}")

    def swap_synthesizer(self, engine: str, speaker: str):
        self.synthesizer = TtsFactory.get_engine(engine, speaker)

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.content.startswith("$"):
            return
        if message.author.id == self.owner.id:
            print(f'Message from {message.author}: {message.content}')
            await self.play_message_in_current_channel(message.content)

    @commands.command()
    async def become(self, ctx: Context, *, member: discord.Member = None):
        member = member or ctx.author
        if member is not self.owner:
            await ctx.send("Ah ah ah, you didn't say the magic word.")
            return

        print("zoop")


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
async def join(ctx: Context, engine, speaker):
    if not bot.get_cog(COG_NAME):
        guild = bot.get_guild(ctx.author.mutual_guilds[0].id)
        member = guild.get_member(ctx.author.id)
        await guild.me.edit(nick=ctx.author.display_name + "-ghost")
        vc = await member.voice.channel.connect()
        speaker = speaker.capitalize()


        if not engine or engine not in ENGINES:
            engine = "elevenlabs"

        if not speaker or speaker not in VOICES:
            # speaker = "21m00Tcm4TlvDq8ikWAM" // rachel
            # speaker = "AZnzlk1XvdvUeBnXmlld" //Domi
            # speaker = "ErXwobaYiN019PkySvjV" //Antoni
            speaker = "TxGEqnHWrfWFTfGW9XjX"

        await bot.add_cog(GhostOwnerCog(bot, ctx.author, vc, engine, speaker))
    else:
        await ctx.send("I'm already in a channel!")

@bot.command()
async def become(ctx, speaker):
    cog: GhostOwnerCog = bot.get_cog()
    cog.swap_synthesizer()

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


