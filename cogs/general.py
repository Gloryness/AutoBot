import discord
from discord.ext import commands
from utils import embeds

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(move_members=True)
    async def move(self, ctx, *, channel):
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

        embed = await embeds.generate_embed(ctx, author, members, method="moved",
                                     title=f'{current_channel.name} ------> {channel}')
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx):
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(mute=True)

        embed = await embeds.generate_embed(ctx, author, members, method="muted", title=channel.name)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(deafen_members=True)
    async def deafen(self, ctx):
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(deafen=True)

        embed = await embeds.generate_embed(ctx, author, members, method="deafened", title=channel.name)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True, deafen_members=True)
    async def shush(self, ctx):
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(mute=True, deafen=True)

        embed = await embeds.generate_embed(ctx, author, members, method="shushed", title=channel.name)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True, deafen_members=True)
    async def unshush(self, ctx):
        author = ctx.message.author
        channel = author.voice.channel
        members = channel.members
        for member in members:
            user = ctx.guild.get_member(member.id)
            await user.edit(mute=False, deafen=False)

        embed = await embeds.generate_embed(ctx, author, members, method="unshushed", title=channel.name)
        await ctx.send(embed=embed)

    @mute.error
    @deafen.error
    @shush.error
    @unshush.error
    async def on_error(self, ctx, error):
        if 'AttributeError' in str(error):
            await ctx.send(":x: You are not connected to a voice call currently!")
        else:
            await ctx.send(f':x: An unexpected error occured. Use `>help` if you are stuck.\nError: `{error}`')

def setup(client):
    client.add_cog(General(client))