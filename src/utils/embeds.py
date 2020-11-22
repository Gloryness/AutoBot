import discord
from itertools import cycle
from discord.ext import commands

class Embeds:
    circles = cycle({
        ':white_circle:',
        ':orange_circle:',
        ':yellow_circle:',
        ':purple_circle:',
        ':green_circle:',
        ':brown_circle:',
        ':blue_circle:',
        ':red_circle:'
    })
    squares = cycle({
        ':white_large_square:',
        ':orange_square:',
        ':yellow_square:',
        ':purple_square:',
        ':green_square:',
        ':brown_square:',
        ':blue_square:',
        ':red_square:'
    })
    hearts = cycle({
        ':white_heart:'
        ':orange_heart:'
        ':yellow_heart:'
        ':purple_heart:'
        ':green_heart:'
        ':brown_heart:'
        ':blue_heart:'
        ':heart:'
    })

    def valid_emoji(self, emoji: str):
        if emoji.count(':') > 2:
            index = emoji.index(':', 2) + 1
            return emoji[0:index]
        return emoji

    async def generate_embed(self, ctx, author, members, method='handled', title="--", emoji="white_check_mark"):
        embed = discord.Embed(title=title,
                              description=f":{emoji}: **{'Uns' if emoji != 'white_check_mark' else 'S'}uccessfully** {method} the following users:",
                              colour=0x38FD41)
        embed.set_thumbnail(url=author.avatar_url)
        if len(members) == 0:
            embed.add_field(name="Error", value="The host is not connected to a voice channel.")
            embed.set_footer(text="AutoBot programmed by Gloryness",
                             icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")
            return embed
        _sep = len(members) // 3
        if _sep == 0:
            _sep = len(members) // 2
            if _sep == 0:
                _sep = len(members) // 1
        rows = [_sep for i in range(_sep, len(members) + 1, _sep)]
        if len(rows) > 3:
            rows = [rows[0], rows[1], rows[2]]
        if sum(rows) < len(members):
            for i in range(abs(len(members) - sum(rows))):
                rows[i] += 1
        elif sum(rows) > len(members):
            for i in range(abs(len(members) - sum(rows))):
                rows[-(i + 1)] -= 1
        users = ''
        for index, member in enumerate(members, start=1):
            user = ctx.guild.get_member(member.id)
            newline = '\n' if users != '' else ''
            if len(rows) == 1:
                users += newline + f'{self.valid_emoji(next(self.circles))} **{user.display_name}#{user.discriminator}**'
                if index == sum(rows):
                    embed.add_field(name="Users", value=users, inline=False)
                    users = ''
            elif len(rows) == 2:
                if (one := (index <= sum([rows[0]]))) or index <= sum(rows):
                    if one:
                        users += newline + f'{self.valid_emoji(next(self.circles))} **{user.display_name}#{user.discriminator}**'
                    else:
                        users += newline + f'{self.valid_emoji(next(self.hearts))} **{user.display_name}#{user.discriminator}**'
                if (one := (index == sum([rows[0]]))) or index == sum(rows):
                    embed.add_field(name="Users", value=users, inline=True)
                    users = ''
            elif len(rows) == 3:
                if (one := (index <= sum([rows[0]]))) or (two := (index <= sum([rows[0], rows[1]]))) or index <= sum(
                        rows):
                    if one:
                        users += newline + f'{self.valid_emoji(next(self.circles))} **{user.display_name}#{user.discriminator}**'
                    elif two:
                        users += newline + f'{self.valid_emoji(next(self.hearts))} **{user.display_name}#{user.discriminator}**'
                    else:
                        users += newline + f'{self.valid_emoji(next(self.squares))} **{user.display_name}#{user.discriminator}**'
                if (one := (index == sum([rows[0]]))) or (two := (index == sum([rows[0], rows[1]]))) or index == sum(
                        rows):
                    embed.add_field(name="Users", value=users, inline=True)
                    users = ''
        embed.set_footer(text="AutoBot programmed by Gloryness",
                         icon_url="https://cdn.discordapp.com/avatars/350963503424733184/46af48be5dcc80d08fd1fbcffc4cfe0a.png?size=128")
        return embed

generate_embed = Embeds().generate_embed