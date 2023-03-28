import logging
from typing import Any

import discord
from boto3 import Session
from discord import VoiceClient, Message, Member, VoiceState, Component, ActionRow, VoiceChannel, Interaction
from discord._types import ClientT
from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot
import os

from dotenv import load_dotenv

from tts.TtsFactory import TtsFactory
from tts.api.TtsEngine import TtsEngine
from tts.elevenlabs.ElevenLabsEngine import ElevenLabsEngine
from tts.polly.PollyEngine import PollyEngine

load_dotenv()

BOT_KEY = os.getenv("BOT_KEY")
ENGINES = ["elevenlabs", "polly"]

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = False

bot: Bot = commands.Bot(command_prefix='$', intents=intents)

BOT_USER_ID = os.getenv("BOT_USER_ID")
COG_NAME = "GhostOwnerCog"


class GhostOwnerCog(Cog):

    def __init__(self, bot: commands.Bot, owner: Member):
        self.bot = bot
        self.owner = owner
        self.synthesizer: TtsEngine = None
        self.voice_channel = None
        self.voice_client = None
        print(f"Cog created in server {owner.guild}!")

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

    def set_voice_channel(self, voice_channel: VoiceChannel):
        self.voice_channel = voice_channel

    async def join_current_voice_channel(self, ctx: Context):
        if self.voice_channel is None:
            await ctx.send("Sorry, I can't join the voice channel you're in, since you aren't in one!")
            return

        if not self.voice_client:
            self.voice_client = await self.voice_channel.connect()
            return

        if self.voice_client and self.voice_client.channel != self.voice_channel:
            print(f"Connecting to channel {self.voice_channel}")
            await self.voice_client.disconnect()
            self.voice_client = await self.voice_channel.connect()
            return

    async def play_message_in_current_channel(self, message_content):
        if not self.synthesizer:
            print("Failure!")
            return

        output = self.synthesizer.get_audio(message_content)
        self.voice_client.play(discord.FFmpegPCMAudio(output))

    async def cog_load(self) -> None:
        """
        Setup Method
        """
        pass
    async def cog_unload(self) -> None:
        """
        Teardown method
        """
        if self.voice_client:
            await self.voice_client.disconnect()
            await self.play_message_in_current_channel("Goodbye!")

    def set_tts_engine(self, ttsEngine: TtsEngine):
        self.synthesizer = ttsEngine


@bot.command()
async def swap(ctx: Context):
    cog = bot.get_cog(COG_NAME)
    if cog:
        await ctx.send(view=SpeakerView(VOICES, cog))
    else:
        await ctx.send("Sorry, no cog available to swap voices on!")


class SpeakerView(discord.ui.View):
    def __init__(self, engines, cog):
        super().__init__()
        self.cog = cog
        self.current_speaker_dropdown = None
        self.add_item(ApiDropDown(engines, self))

    def api_selected(self, option):
        if self.current_speaker_dropdown:
            self.remove_item(self.current_speaker_dropdown)

        engine = option
        print(f"Found engine {engine} selected, adding dropdown for it.")
        if engine.lower() == "polly":
            voices = PollyEngine.get_speaker_dict()
        elif engine.lower() == "elevenlabs":
            voices = ElevenLabsEngine.get_speaker_dict()
        else:
            voices = {}

        self.add_item(SpeakerDropdown(engine, voices, cog=self.cog))



class ApiDropDown(discord.ui.Select):
    def __init__(self, engines: list, parent: SpeakerView):
        self.parent_view = parent
        options = [self._generate_api_option(engine) for engine in engines]
        super().__init__(placeholder="Select an API", options=options)

    def _generate_api_option(self, engine):
        return discord.SelectOption(label=engine, value=engine)

    async def callback(self, interaction: Interaction[ClientT]) -> Any:
        option = self.values[0]
        self.parent_view.api_selected(option)
        await interaction.message.edit(view=self.parent_view)
        return


class SpeakerDropdown(discord.ui.Select):
    def __init__(self, engine, speakers_for_api: dict, cog):
        options = [self._generate_speaker_option(display, identifier) for display, identifier in speakers_for_api.items()]
        self.engine = engine
        self.cog: GhostOwnerCog = cog
        super().__init__(placeholder="Choose your speaker", options=options)

    async def callback(self, interaction: discord.Interaction):
        for option in self.options:
            if option.value == self.values[0]:
                name = option.label
                engine = TtsFactory.get_engine(self.engine, self.values[0])
                self.cog.set_tts_engine(engine)
                await bot.add_cog(self.cog)
                await interaction.response.send_message(f'OK, I am  now {name}')


    def _generate_speaker_option(self, display, identifier):
        return discord.SelectOption(label=display, value=identifier, description=display + "woo", emoji='🟥')


@bot.command()
async def join2(ctx: Context):
    cog = bot.get_cog(COG_NAME)
    if cog:
        guild = bot.get_guild(ctx.author.mutual_guilds[0].id)
        member = guild.get_member(ctx.author.id)
        await guild.me.edit(nick=ctx.author.display_name + "-ghost")
        channel = member.voice.channel
        cog.set_voice_channel(channel)
        await cog.join_current_voice_channel(ctx)
    else:
        print("zoop")


@bot.command()
async def init(ctx: Context):
    if not bot.get_cog(COG_NAME):
        guild = bot.get_guild(ctx.author.mutual_guilds[0].id)
        member = guild.get_member(ctx.author.id)
        await guild.me.edit(nick=ctx.author.display_name + "-ghost")
        voice_channel = member.voice.channel
        cog = GhostOwnerCog(bot, member)
        await ctx.send(view=SpeakerView(ENGINES, cog))


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
