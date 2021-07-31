import db
import discord

async def list_all_events(ctx):
    event_dates = db.event_dates
    present_users = db.present_users

    embed = discord.Embed(title='Upcoming Events', color=0x00FF00)
    for i in range(len(event_dates)):
        present_usernames = ''
        for present_user in present_users[i]:
            present_usernames += present_user.display_name + '\n'
        embed.add_field(name=event_dates[i].strftime('%d.%m. %H:%M'), value=present_usernames, inline=True)

    await ctx.channel.send(embed=embed)