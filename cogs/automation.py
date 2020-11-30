import time
import discord
from discord.ext import commands
import colorama
from utils import embeds

class Automation(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.questions = [
            'A brief description of the subject (e.g **Among Us**, **Movie Night**, **Skribbl.io**)\n'
            '**NOTE:** You can type `skip` to skip any question, including the ones that include voice channels.',
            'What is the maximum amount of people that can participate?',
            'What is the name/id of the waiting room Voice Channel?\n'
            '**NOTE:** If you skip this question, the `>start` command will no longer be '
            'available as it is meant to transfer everyone that\'s in the waiting room to the vc.',
            'What is the name/id of the Voice Channel it will take place in?',
            'When will it start? (**now**, **10mins**, **etc**)',
            'What role would you like to ping for the announcement? '
            '(**everyone**, **here**, **none**, **etc** - you can also use the **ID** of the role.)',
            'What channel would you like this announcement to be sent in?'
        ]
        self.descriptions = [
            ':notepad_spiral: Description',
            ':stop_sign: Maximum People',
            ':clock4: Waiting Room',
            ':speaker: Voice Channel',
            ':alarm_clock: Starts'
        ]

    def delete_attributes(self, guild_id, user_id):
        attributes = [
            "author",
            "guild",
            "channel",
            "subject",
            "embed",
            "waiting",
            "question",
            "questions",
            "descriptions",
            "announcement_id",
            "announcement_channel",
            "waiting_room_not_given",
            "waiting_room",
            "voice_channel",
            "role_to_ping",
            "setup_value"
        ]

        for attribute in attributes:
            try:
                delattr(self, f'{attribute}{guild_id}{user_id}') # Cleaning up the user's attributes since we no longer need them.
            except:
                pass

    @commands.command(pass_context=True)
    async def start(self, ctx):
        """
        Used to start and move everyone from the given waiting-room to the actual VC the announcement takes place in.
        An error will occur if the host is not in the waiting-room.
        """
        id_ = ctx.author.id
        guild_id = ctx.guild.id
        if not hasattr(self, f'announcement_id{guild_id}{id_}'):
            # await ctx.send(':x: You have not setup anything yet! Use `>help` if you are stuck.')
            embed = await embeds.generate_embed(ctx, ctx.message.author, [],
                                                description=':x: Could not perform action:',
                                                title=f'Error!',
                                                error_reason="You have not setup anything yet! Use `>help` if you are stuck."
                                                )
            await ctx.send(embed=embed)
            return
        voice_channel = getattr(self, f'voice_channel{guild_id}{id_}')
        waiting_room = getattr(self, f'waiting_room{guild_id}{id_}')
        voice_channels = ctx.guild.voice_channels
        msg = await getattr(self, f'announcement_channel{guild_id}{id_}').fetch_message(getattr(self, f'announcement_id{guild_id}{id_}'))
        reactions = msg.reactions[0]
        users = await reactions.users().flatten() # flattening it into a list
        for user in users:
            if user.display_name == 'AutoBot':
                continue
            for vc in voice_channels:
                if vc.name == voice_channel or str(vc.id) == str(voice_channel):
                    try:
                        await user.edit(voice_channel=vc)
                    except:
                        continue
        try:
            members = ctx.message.author.voice.channel.members
        except AttributeError:
            members = []
        embed = await embeds.generate_embed(ctx, ctx.message.author, members,
                                            description=":white_check_mark: Successfully moved the following users:",
                                            title=f'{waiting_room} ------> {voice_channel}',
                                            error_reason="The host is not connected to a voice channel."
                                            )

        await ctx.send(embed=embed)
        self.delete_attributes(guild_id, ctx.author.id)

    @commands.command(pass_context=True)
    async def setup(self, ctx, *, subject: str):
        """
        Used to setup what the announcement is going to about.
        :param subject: Subject of what it's about (Game, Event)
        """
        id_ = ctx.author.id
        guild_id = ctx.guild.id
        if hasattr(self, f'author{guild_id}{id_}'):
            await ctx.send(':x: There is an event already happening - cannot perform this action right now!')
            return
        setattr(self, f'waiting{guild_id}{id_}', False)
        setattr(self, f'setup_value{guild_id}{id_}', dict(zip(self.descriptions, ["" for i in range(len(self.descriptions))])))
        setattr(self, f'question{guild_id}{id_}', "")
        setattr(self, f'voice_channel{guild_id}{id_}', "")
        setattr(self, f'waiting_room{guild_id}{id_}', "")

        setattr(self, f'author{guild_id}{id_}', ctx.message.author)
        setattr(self, f'guild{guild_id}{id_}', guild_id)
        setattr(self, f'channel{guild_id}{id_}', ctx.message.channel)
        setattr(self, f'subject{guild_id}{id_}', subject.title())
        setattr(self, f'embed{guild_id}{id_}', discord.Embed(title="Attention!",
                                   description=":white_check_mark: React to this message if you are willing to join in!\n"
                                                ":speaking_head: Please remember to join the given **Waiting Room** "
                                               "voice channel **IF AVAILABLE.**.",
                                   colour=0xFFAE00))
        embed = getattr(self, f'embed{guild_id}{id_}')
        author = getattr(self, f'author{guild_id}{id_}')
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text="AutoBot programmed by Gloryness",
                         icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")

        setattr(self, f'waiting{guild_id}{id_}', True)
        setattr(self, f'questions{guild_id}{id_}', iter(self.questions))
        setattr(self, f'descriptions{guild_id}{id_}', iter(self.descriptions))
        await ctx.send(next(getattr(self, f'questions{guild_id}{id_}')))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        id_ = message.author.id
        msg = message.content
        guild_id = message.guild.id
        print(f'"{colorama.Fore.LIGHTGREEN_EX}{message.guild.name}{colorama.Fore.RESET}" --- '
              f'{colorama.Style.BRIGHT}{colorama.Fore.RED}{message.author.display_name} '
              f'{colorama.Style.RESET_ALL}{colorama.Fore.LIGHTBLUE_EX}in #{message.channel.name}{colorama.Fore.RESET} --- '
              f'{colorama.Fore.YELLOW}Today at {time.ctime(time.time())[11:-5]}{colorama.Fore.RESET} --- '
              f'{colorama.Fore.MAGENTA}{msg}{colorama.Fore.RESET}')
        try:
            author = getattr(self, f'author{guild_id}{id_}')
            channel = getattr(self, f'channel{guild_id}{id_}')
            embed = getattr(self, f'embed{guild_id}{id_}')
            subject = getattr(self, f'subject{guild_id}{id_}')
            question = getattr(self, f'question{guild_id}{id_}')
            if hasattr(self, f'waiting{guild_id}{id_}') and not msg.startswith('>'):
                if message.author == author and message.channel == channel and getattr(self, f'waiting{guild_id}{id_}'):
                    channel = message.channel
                    if question.startswith('What role'):
                        done = False
                        for role in message.guild.roles:
                            if message.content.lower() == 'none':
                                setattr(self, f'role_to_ping{guild_id}{id_}', '')
                                done = True
                                break
                            elif message.content.lower() in ['everyone', 'here']:
                                setattr(self, f'role_to_ping{guild_id}{id_}', '@'+message.content.lower())
                                done = True
                                break
                            if role.name == message.content or str(role.id) == str(message.content):
                                setattr(self, f'role_to_ping{guild_id}{id_}', role.mention)
                                done = True
                        if not done:
                            channel.send(':x: Invalid role.')

                    if (one := question.__contains__('Voice Channel it will')) or (two := question.__contains__('waiting room')):
                        if msg.lower() != 'skip':
                            if one:
                                if msg.lower() == 'skip':
                                    await channel.send(':x: Cannot skip this question.')
                                setattr(self, f'voice_channel{guild_id}{id_}', msg)
                                voice = getattr(self, f'voice_channel{guild_id}{id_}')
                            elif two:
                                setattr(self, f'waiting_room{guild_id}{id_}', msg)
                                voice = getattr(self, f'waiting_room{guild_id}{id_}')
                            if getattr(self, f'voice_channel{guild_id}{id_}').isdigit():
                                for vc in message.guild.voice_channels:
                                    if int(vc.id) == int(getattr(self, f'voice_channel{guild_id}{id_}')):
                                        setattr(self, f'voice_channel{guild_id}{id_}', vc.name)
                                        voice = getattr(self, f'voice_channel{id}')
                                        break
                            elif getattr(self, f'waiting_room{guild_id}{id_}').isdigit():
                                for vc in message.guild.voice_channels:
                                    if int(vc.id) == int(getattr(self, f'waiting_room{guild_id}{id_}')):
                                        setattr(self, f'waiting_room{guild_id}{id_}', vc.name)
                                        voice = getattr(self, f'waiting_room{id}')
                                        break
                            msg = voice
                            voice_channels = message.guild.voice_channels
                            done = False
                            for vc in voice_channels:
                                if vc.name == voice:
                                    done = True
                                    invite = await vc.create_invite(unique=False, reason='Automated by using >setup')
                                    msg = msg.replace(vc.name, f"[{vc.name}]({invite})")
                                    break
                            if not done:
                                await channel.send(":x: Invalid voice channel name.")
                                return

                    if 'two' not in locals():
                        two = False

                    if not msg.startswith('<#') and not question.startswith('What role'):
                        if msg.lower() == 'skip' and two:
                            desc = str(next(getattr(self, f"descriptions{guild_id}{id_}"))) # skipping the waiting room description
                            setup_value = getattr(self, f'setup_value{guild_id}{id_}')
                            del setup_value[desc]
                            setattr(self, f"waiting_room_not_given{guild_id}{id_}", True)
                        else:
                            if msg.lower() == 'skip':
                                msg = 'No info available'
                            desc = str(next(getattr(self, f"descriptions{guild_id}{id_}")))
                            setup_value = getattr(self, f'setup_value{guild_id}{id_}')
                            setup_value[desc] = msg
                            setattr(self, f'setup_value{guild_id}{id_}', setup_value)

                    setattr(self, f'question{guild_id}{id_}', str(next(getattr(self, f"questions{guild_id}{id_}"))))
                    await channel.send(getattr(self, f'question{guild_id}{id_}'))
        except StopIteration:
            setup_value = getattr(self, f'setup_value{guild_id}{id_}')
            setattr(self, f'questions{guild_id}{id_}', iter(self.questions))
            setattr(self, f'descriptions{guild_id}{id_}', iter(self.descriptions))
            setattr(self, f'waiting{guild_id}{id_}', False)
            setattr(self, f'announcement_channel{guild_id}{id_}', self.client.get_channel(int(message.content.strip('<#>'))))
            embed.add_field(name=f"Subject: {subject}", value='\n'.join([f'{key}: **{setup_value[key]}**' for key in setup_value]), inline=False)
            msg = await getattr(self, f'announcement_channel{guild_id}{id_}').send(getattr(self, f'role_to_ping{guild_id}{id_}'), embed=embed)
            await msg.add_reaction("\U00002705") # :white_check_mark:
            setattr(self, f'announcement_id{guild_id}{id_}', msg.id)
            setattr(self, f'setup_value{guild_id}{id_}', dict(zip(self.descriptions, ["" for i in range(len(self.descriptions))])))
            if hasattr(self, f"waiting_room_not_given{guild_id}{id_}"):
                self.delete_attributes(guild_id, id_)
        except AttributeError:
            pass

    @start.error
    @setup.error
    async def on_error(self, ctx, error):
        """
        Handles the errors.
        """
        id_ = ctx.author.id
        guild_id = ctx.guild.id
        setattr(self, f'questions{guild_id}{id_}', iter(self.questions))
        setattr(self, f'descriptions{guild_id}{id_}', iter(self.descriptions))
        setattr(self, f'waiting{guild_id}{id_}', False)
        setattr(self, f'setup_value{guild_id}{id_}', dict(zip(self.descriptions, ["" for i in range(len(self.descriptions))])))
        await ctx.send(f':x: An error occured!\nError: `{error}`')

def setup(client):
    client.add_cog(Automation(client))