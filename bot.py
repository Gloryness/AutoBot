import os
import discord
import traceback
from discord.ext import commands
from utils.cache import Cache

def get_prefix(client, message):
    cache = Cache('prefixes.json')
    data = cache.all()
    return data[str(message.guild.id)]

tokenfile = open('token.txt')
token = tokenfile.read().strip()
tokenfile.close()

intents = discord.Intents()
client = commands.Bot(command_prefix=get_prefix, intents=intents.all(), help_command=None)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name="everything", type=discord.ActivityType.watching))
    print('Bot is online.')
    print('The servers that I\'m in are:')
    for guild in client.guilds:
        print(f"- {guild.name} ({guild.id}) ----- Owned by {guild.owner.display_name} with {guild.member_count} members -- "
              f"{', '.join(map(lambda k: k.display_name, guild.members))}")

@client.event
async def on_guild_join(guild):
    cache = Cache('prefixes.json')
    data = cache.all()

    data[str(guild.id)] = '>'

    cache.store(data)

@client.event
async def on_guild_remove(guild):
    cache = Cache('prefixes.json')
    data = cache.all()

    data.pop(str(guild.id))

    cache.store(data)

@client.command(aliases=['help', 'h'], pass_context=True)
async def _help(ctx):
    general_message = "`>shush` - Mutes and deafens everyone in the current VC.\n" \
                   "`>unshush` - Unmutes and undeafens everyone in the current VC.\n" \
                   "`>mute` - Mutes everyone in the current VC.\n" \
                   "`>deafen` - Deafens everyone in the current VC.\n" \
                   "`>move {voice_channel_name}` - Move everyone in the current VC to another VC."
    automation_message = "`>setup {subject}` - Make an announcement about something that's happening (e.g events, movies, games)\n" \
                         "`>start` - Make everyone that reacted to the announcement to join the given Voice Channel (must be in waiting-room)."
    moderator_message = '`>history {user} {channel} {limit}` - Shows the message history of a user. (max limit: 50)\n' \
                        '`>changeprefix {prefix}` - Changes the bots prefix.'
    developer_message = "`>extension load {extension_name}` - Loads up an extension.\n" \
                        "`>extension unload {extension_name}` - Unloads an extension.\n" \
                        "`>extension reload {extension_name}` - Reloads an extension."
    external_message = "If you want to check out the source code so you can see how the " \
                       "bot works, check out the github [here](https://github.com/Goryness/AutoBot)."

    author = ctx.message.author
    embed = discord.Embed(title="Help", description=f"**Command Prefix: `{get_prefix(client, ctx)}`**", colour=0xFB94F0)
    embed.set_thumbnail(url=author.avatar_url)
    embed.add_field(name="-- General --", value=general_message, inline=False)
    embed.add_field(name="\n-- Automation --", value=automation_message, inline=False)
    embed.add_field(name="\n-- Moderator --", value=moderator_message, inline=False)
    embed.add_field(name="\n-- Developer --", value=developer_message, inline=False)
    embed.add_field(name="\n-- External --", value=external_message, inline=False)
    embed.set_footer(text="AutoBot programmed by Gloryness",
                     icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")

    await ctx.send(embed=embed)

def is_a_developer(ctx):
    return ctx.author.id in [350963503424733184]

@client.group(aliases=['ext'])
async def extension(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid extension command passed. **Use `>help` for help.**')

@extension.command()
@commands.check(is_a_developer)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'**{extension}** was successfully loaded. :white_check_mark:')

@extension.command()
@commands.check(is_a_developer)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'**{extension}** was successfully unloaded. :white_check_mark:')

@extension.command()
@commands.check(is_a_developer)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'**{extension}** was successfully reloaded. :white_check_mark:')

@load.error
@unload.error
@reload.error
async def extension_error(ctx, error):
    if 'ExtensionAlreadyLoaded' in traceback.format_exc():
        await ctx.send(':x: Extension has already been loaded! :angry:')
    elif 'ExtensionNotLoaded' in traceback.format_exc():
        await ctx.send(':x: Extension has not been loaded yet! :angry:')
    elif 'ExtensionNotFound' in traceback.format_exc():
        await ctx.send(':x: Extension not found.')
    elif 'CheckFailure' in traceback.format_exc():
        await ctx.send(':x: Insufficient permissions.')
    else:
        await ctx.send(f':x: **An error has occured.**\nError: `{error}`')

for filename in filter(lambda k: k.endswith('.py'), os.listdir('./cogs')):
    client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)