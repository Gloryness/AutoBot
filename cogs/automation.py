import discord
from discord.ext import commands
from utils import embeds

class Automation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.setup_value = ':notepad_spiral: Description: '
        self.waiting = False
        self.question = ""
        self.voice_channel = ""
        self.waiting_room = ""
        self.questions_ = [
            'A brief description of the subject (e.g **Among Us**, **Movie Night**, **Skribbl.io**)',
            'What is the maximum amount of people that can participate?',
            'What is the name/id of the waiting room Voice Channel?',
            'What is the name/id of the Voice Channel it will take place in?',
            'When will it start?',
            'What role would you like to ping for the announcement? '
            '(**everyone**, **here**, **none**, **etc** - you can also use the **ID** of the role.)',
            'What channel would you like this announcement to be sent in?'
        ]
        self.descriptions_ = [
            '\n:stop_sign: Maximum People: ',
            '\n:clock4: Waiting Room: ',
            '\n:speaker: Voice Channel: ',
            '\n:alarm_clock: Starts: ',
            ''
        ]

    @commands.command(pass_context=True)
    async def start(self, ctx):
        voice_channels = ctx.guild.voice_channels
        if not hasattr(self, 'announcement_id'):
            await ctx.send(':x: You have not setup anything yet! Use `>help` if you are stuck.')
            return
        msg = await self.announcement_channel.fetch_message(self.announcement_id)
        reactions = msg.reactions[0]
        users = await reactions.users().flatten()
        for user in users:
            if user.display_name == 'AutoBot':
                continue
            for vc in voice_channels:
                if vc.name == self.voice_channel or str(vc.id) == str(self.voice_channel):
                    try:
                        await user.edit(voice_channel=vc)
                    except:
                        continue
        delattr(self, 'announcement_id')
        delattr(self, 'author')

        try:
            members = ctx.message.author.voice.channel.members
        except AttributeError:
            members = []
        embed = await embeds.generate_embed(ctx, ctx.message.author, members, method="moved", emoji="white_check_mark" if members != [] else "x",
                                            title=f'{self.waiting_room} ------> {self.voice_channel}')

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def setup(self, ctx, subject: str):
        if hasattr(self, 'author'):
            await ctx.send(':x: There is an event already happening - cannot perform this action right now!')
            return
        self.author = ctx.message.author
        self.subject = subject.title()
        self.embed = discord.Embed(title="Attention!",
                                   description=":white_check_mark: React to this message if you are willing to join in!\n"
                                                ":speaking_head: Please remember to join the given **Waiting Room** voice channel.",
                                   colour=0xFFAE00)
        self.embed.set_thumbnail(url=self.author.avatar_url)
        self.embed.set_footer(text="AutoBot programmed by Gloryness",
                         icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")
        self.waiting = True
        self.questions = iter(self.questions_)
        self.descriptions = iter(self.descriptions_)
        await ctx.send(next(self.questions))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        msg = message.content
        try:
            if self.waiting and not msg.startswith('>'):
                if message.author == self.author:
                    channel = message.channel
                    if self.question.startswith('What role'):
                        done = False
                        for role in message.guild.roles:
                            if message.content.lower() == 'none':
                                self.role_to_ping = ''
                                done = True
                                break
                            elif message.content.lower() in ['everyone', 'here']:
                                self.role_to_ping = '@'+message.content.lower()
                                done = True
                                break
                            if role.name == message.content or str(role.id) == str(message.content):
                                self.role_to_ping = role.mention
                                done = True
                        if not done:
                            channel.send(':x: Invalid role.')

                    if (one := self.question.__contains__('Voice Channel it will')) or (two := self.question.__contains__('waiting room')):
                        if one:
                            voice = self.voice_channel = msg
                        elif two:
                            voice = self.waiting_room = msg
                        if self.voice_channel.isdigit():
                            for vc in message.guild.voice_channels:
                                if int(vc.id) == int(self.voice_channel):
                                    voice = self.voice_channel = vc.name
                                    break
                        elif self.waiting_room.isdigit():
                            for vc in message.guild.voice_channels:
                                if int(vc.id) == int(self.waiting_room):
                                    voice = self.waiting_room = vc.name
                                    break
                        msg = voice
                        voice_channels = message.guild.voice_channels
                        done = False
                        for vc in voice_channels:
                            if vc.name == voice:
                                done = True
                        if not done:
                            await channel.send(":x: Invalid voice channel name.")
                            return

                    if not msg.startswith('<#') and not self.question.startswith('What role'):
                        self.setup_value += f'**{msg}**{next(self.descriptions)}'

                    self.question = str(next(self.questions))
                    await channel.send(self.question)
        except StopIteration:
            self.questions = iter(self.questions_)
            self.descriptions = iter(self.descriptions_)
            self.waiting = False
            self.announcement_channel = self.client.get_channel(int(message.content.strip('<#>')))
            self.embed.add_field(name=f"Subject: {self.subject}", value=self.setup_value, inline=False)
            msg = await self.announcement_channel.send(self.role_to_ping, embed=self.embed)
            await msg.add_reaction("\U00002705") # :white_check_mark:
            self.announcement_id = msg.id
            self.setup_value = ':notepad_spiral: Description: '

    @start.error
    @setup.error
    async def on_error(self, ctx, error):
        self.questions = iter(self.questions_)
        self.descriptions = iter(self.descriptions_)
        self.setup_value = ':notepad_spiral: Description: '
        self.waiting = False
        await ctx.send(f':x: An error occured!\nError: `{error}`')

def setup(client):
    client.add_cog(Automation(client))