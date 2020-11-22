import os
import discord
from discord.ext import commands

tokenfile = open('token.txt')
token = tokenfile.read().strip()
tokenfile.close()

intents = discord.Intents()
client = commands.Bot(command_prefix='>', intents=intents.all(), help_command=None)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name="everything", type=discord.ActivityType.watching))
    print('Bot is online.')

@client.command(aliases=['help', 'h'], pass_context=True)
async def _help(ctx):
    general_message = "`>shush` - Mutes and deafens everyone in the current VC.\n" \
                   "`>unshush` - Unmutes and undeafens everyone in the current VC.\n" \
                   "`>mute` - Mutes everyone in the current VC.\n" \
                   "`>deafen` - Deafens everyone in the current VC.\n" \
                   "`>move channel_name` - Move everyone in the current VC to another VC."
    automation_message = "`>setup {subject}` - Make an announcement about something that's happening (e.g events, movies, games)\n" \
                         "`>start` - Make everyone that reacted to the announcement to join the given Voice Channel (must be in waiting-room)."
    external_message = "If you want to check out the source code so you can see how the " \
                       "bot works, check out the github [here](https://github.com/Goryness/AutoBot)."
    developer_message = "`>extension load {extension_name}` - Loads up an extension.\n" \
                        "`>extension unload {extension_name}` - Unloads an extension.\n" \
                        "`>extension reload {extension_name}` - Reloads an extension."
    author = ctx.message.author
    embed = discord.Embed(title="Help", description="**Command Prefix: `>`**", colour=0xFB94F0)
    embed.set_thumbnail(url=author.avatar_url)
    embed.add_field(name="-- General --", value=general_message, inline=False)
    embed.add_field(name="\n-- Automation --", value=automation_message, inline=False)
    embed.add_field(name="\n-- Developer --", value=developer_message, inline=False)
    embed.add_field(name="\n-- External --", value=external_message, inline=False)
    embed.set_footer(text="AutoBot programmed by Gloryness",
                     icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")

    await ctx.send(embed=embed)

@client.group()
async def extension(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid extension command passed. **Use `>help` for help.**')

@extension.command()
@commands.has_role(item='Bot Developer')
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'**{extension}** was successfully loaded. :white_check_mark:')

@extension.command()
@commands.has_role(item='Bot Developer')
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'**{extension}** was successfully unloaded. :white_check_mark:')

@extension.command()
@commands.has_role(item='Bot Developer')
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'**{extension}** was successfully reloaded. :white_check_mark:')

@load.error
@unload.error
@reload.error
async def extension_error(ctx, error):
    if 'ExtensionAlreadyLoaded' in str(error):
        await ctx.send('Extension has already been loaded! :angry:')
    elif 'ExtensionNotLoaded' in str(error):
        await ctx.send('Extension has not been loaded yet! :angry:')
    elif 'ExtensionNotFound' in str(error):
        await ctx.send('Extension not found.')
    else:
        await ctx.send(f':x: **An error has occured.**\nError: `{error}`')

for filename in filter(lambda k: k.endswith('.py'), os.listdir('./cogs')):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)