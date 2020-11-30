import traceback
import discord
from discord.ext import commands
from utils import embeds
from utils.cache import Cache

class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix_cache = Cache('prefixes.json')

    @commands.command()
    @commands.has_permissions(read_messages=True)
    @commands.bot_has_permissions(read_messages=True)
    async def history(self, ctx: commands.Context, user: discord.Member, channel: discord.TextChannel, limit=50):
        if limit > 50: # to reduce the embed being too long
            limit = 50

        while True:
            history = list(reversed(list(filter(lambda msg: msg.author.display_name == user.display_name,
                             await channel.history(limit=limit).flatten()))))
            if len(history) == 0:
                limit += 100
            else:
                break
        embed = discord.Embed(title="History",
                              description=f"**{user.display_name}**'s last {limit} messages in #{channel.name}:",
                              colour=0xFFBA00)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text="AutoBot programmed by Gloryness",
                         icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")

        for index, message in enumerate(history):
            embed.add_field(name=str(message.created_at)[0:-7], value=message.content, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_guild=True)
    async def changeprefix(self, ctx, prefix):
        data = self.prefix_cache.all()

        data[str(ctx.guild.id)] = prefix

        self.prefix_cache.store(data)

        await ctx.send(f':white_check_mark: Prefix successfully changed to: **`{prefix}`**')

    async def on_error(self, ctx, error):
        if 'BotMissingPermissions' in traceback.format_exc():
            reason = ':x: I cannot perform this action as I don\'t have the correct permissions.'
        elif 'MissingPermissions' in traceback.format_exc():
            reason = ':x: Insufficient permissions.'
        else:
            reason = f':x: An unexpected error occured. Use `>help` if you are stuck.\n\nError:\n```css\n{error}```'
        embed = await embeds.generate_embed(ctx, ctx.message.author, [],
                                            description=':x: Could not perform command.',
                                            title=f'Error!',
                                            error_reason=reason
                                            )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderator(client))