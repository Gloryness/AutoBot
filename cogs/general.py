import traceback
from discord.ext import commands
from utils import embeds

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(move_members=True)
    @commands.bot_has_permissions(move_members=True)
    async def move(self, ctx, *, channel):
        """
         Move everyone in the current vc your in to another vc
        :param channel: Channel name or id
        """
        author = ctx.message.author
        current_channel = author.voice.channel
        voice_channels = ctx.guild.voice_channels
        members = current_channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            done = False
            for vc in voice_channels:
                if vc.name == channel or str(vc.id) == str(channel):
                    if channel.isdigit():
                        channel = vc.name
                    done = True
                    await user.edit(voice_channel=vc)
            if not done:
                await ctx.send(":x: Invalid voice channel name.")
                return

        embed = await embeds.generate_embed(ctx, author, members,
                                            description=":white_check_mark: Successfully moved the following users:",
                                            title=f'{current_channel.name} ------> {channel}')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True)
    @commands.bot_has_permissions(mute_members=True)
    async def mute(self, ctx):
        """
        Mute everyone in the current VC that you're in.
        """
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(mute=True)

        embed = await embeds.generate_embed(ctx, author, members,
                                            description=":white_check_mark: Successfully muted the following users:",
                                            title=channel.name)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(deafen_members=True)
    @commands.bot_has_permissions(deafen_members=True)
    async def deafen(self, ctx):
        """
        Deafen everyone in the current VC that you're in.
        """
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(deafen=True)

        embed = await embeds.generate_embed(ctx, author, members,
                                            description=":white_check_mark: Successfully deafened the following users:",
                                            title=channel.name)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True, deafen_members=True)
    @commands.bot_has_permissions(mute_members=True, deafen_members=True)
    async def shush(self, ctx):
        """
        Mute and deafen everyone in the current VC that you're in.
        """
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(mute=True, deafen=True)

        embed = await embeds.generate_embed(ctx, author, members,
                                            description=":white_check_mark: Successfully shushed the following users:",
                                            title=channel.name)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True, deafen_members=True)
    @commands.bot_has_permissions(mute_members=True, deafen_members=True)
    async def unshush(self, ctx):
        """
        Unmute and undeafen everyone in the current VC that you're in.
        """
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(mute=False, deafen=False)

        embed = await embeds.generate_embed(ctx, author, members,
                                            description=":white_check_mark: Successfully unshushed the following users:",
                                            title=channel.name)
        await ctx.send(embed=embed)

    @move.error
    @mute.error
    @deafen.error
    @shush.error
    @unshush.error
    async def on_error(self, ctx, error):
        if 'AttributeError' in traceback.format_exc():
            reason = ":x: You are not connected to a voice call currently!"
        elif 'BotMissingPermissions' in traceback.format_exc():
            reason = ':x: I cannot perform this action as I don\'t have the correct permissions.'
        elif 'MissingPermissions' in traceback.format_exc():
            reason = ':x: Insufficient permissions.'
        else:
            reason = f":x: An unexpected error occured. Use `>help` if you are stuck.\n\nError:\n```css\n{error}```"
        embed = await embeds.generate_embed(ctx, ctx.message.author, [],
                        description=':x: Could not perform command.',
                        title=f'Error!',
                        error_reason=reason
                        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(General(client))