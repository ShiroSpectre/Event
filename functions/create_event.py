import db
import time
import asyncio
import discord
import datetime
from functions import leaderboard_func
from dateparser.search import search_dates as parse

finish = db.finish
refresh = db.refresh
mention = db.mention
role_ID = db.reminder_role
embed_color = db.embed_color
maybe_reminder = db.maybe_reminder

async def create(ctx, args):
    title = (' ').join(args)

    args = list(args)
    if len(args) == 0:
        await ctx.channel.send('missing arguments -> canceling event creation', delete_after=5)
        return
    
    date = parse_date(args)
    if date is None:
        await ctx.channel.send('can not detect event date -> canceling event creation', delete_after=5)
        return

    if (int(time.time()) - db.last_message_time) > mention or ctx.channel != db.last_channel:
        await ctx.channel.send(f'<@&{role_ID}>')
        db.last_message_time = int(time.time())
        db.last_channel = ctx.channel

    for role in ctx.guild.roles:
        if role.id == role_ID:
            members = role.members

    description = f'''
    {title}
    missing votes: {len(members)}/{len(members)} | reminder in X | {date.strftime('%d.%m. %H:%M')}
    '''
    embed = discord.Embed(description=description, color=embed_color)
    msg = await ctx.channel.send(embed=embed)

    channel = ctx.channel
    await update_embed(msg, title, date, members, channel, start_time=int(time.time()), i=1, maybe_reminded=False, date_appended=False)


# helper functions
def parse_date(args):
    # detect today, lazy datetime, single digits and german date specification
    weekday_num = datetime.datetime.today().weekday()
    for i in range(len(args)):
        if args[i].lower() in switch(weekday_num):
            args[i] = 'heute'
        if args[i].lower() == 'uhr':
            if not ':' in args[i-1]:
                args[i-1] += ':00'
        if args[i].isdigit():
            if 1 <= int(args[i]) <= 9:
                args[i] = 'XXX'

    settings={'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY', 'PREFER_LOCALE_DATE_ORDER': False}
    matches = parse((' ').join(args), languages=['de'], settings=settings)

    if matches is not None: return matches[-1][1]


def switch(argument):
    switcher = {
        0: 'montag',
        1: 'dienstag',
        2: 'mittwoch',
        3: 'donnerstag',
        4: 'freitag',
        5: 'samstag',
        6: 'sonntag',
    }
    return switcher.get(argument, "Invalid day")


async def update_embed(msg, title, date, members, channel, start_time, i, maybe_reminded, date_appended):
    # get reaction users
    reaction_list = []
    maybe_list = []
    message = await msg.channel.fetch_message(msg.id)
    for reaction in message.reactions:
        if reaction.emoji == '❌':
            embed = discord.Embed(description='Event deleted', color=0xFF0000)
            await msg.edit(embed=embed, delete_after=5)
            return
        if reaction.emoji == '🤏':
            async for user in reaction.users():
                maybe_list.append(user)
        else:
            async for user in reaction.users():
                reaction_list.append(user)
            present_users = []
            if reaction.emoji != '👎 ':
                async for user in reaction.users():
                    present_users.append(user)
                if len(present_users) >= 5 and not date_appended: #5
                    db.event_dates.append(date)
                    db.present_users.append(present_users)
                    date_appended = True
                    if channel.id != db.prime_channel: 
                        main_channel = db.bot.get_channel(id=db.main_channel)
                        await main_channel.send(f"```\n5 at {date.strftime('%d.%m. %H:%M')}\n```")
    remaining_user = [x for x in members if x not in reaction_list and x not in maybe_list]

    # calculate reminder time
    event_date = time.mktime(date.timetuple())
    remaining_time = int((i*(event_date - start_time)/3) - (time.time()-start_time))

    # edit embed
    description = f'''
    {title}
    missing votes: {len(remaining_user)}/{len(members)} | reminder in {round((remaining_time/3600), 2)} h | {date.strftime('%d.%m. %H:%M')}
    '''
    embed = discord.Embed(description=description, color=embed_color)
    await msg.edit(embed=embed)

    #remind user the second time
    if remaining_time < 0 and (i == 1 or i == 2):
        print('sending reminder')
        await send_reminder(remaining_user, title, channel)
        await leaderboard_func.add_point(remaining_user)
        i += 1
    
    if int(event_date-time.time()) < maybe_reminder and not maybe_reminded:
        print('sending maybe reminder')
        await send_reminder(maybe_list, title, channel, maybe=True)
        maybe_reminded = True
        await leaderboard_func.add_point(maybe_list)

    # finish intervall
    if remaining_user == 0 and maybe_list == 0:
        print('Stopping event')
        embed = discord.Embed(description=title, color=0x00FF00)
        await msg.edit(embed=embed)
        return


    if int(event_date-time.time()) < finish: 
        print('Fnished event')
        embed = discord.Embed(description=title, color=embed_color)
        await msg.edit(embed=embed)

        await leaderboard_func.add_point(remaining_user)
        await leaderboard_func.add_point(maybe_list)  
        return

    await asyncio.sleep(refresh)
    await update_embed(msg, title, date, members, channel, start_time, i, maybe_reminded, date_appended)

async def send_reminder(reminder_list, title, channel, maybe=False):
    for user in reminder_list:
        if not user.bot and not maybe: await user.send(f'Missing vote on event: **{title}** in {channel.mention} -> *adding point to leaderboard*')
        elif not user.bot: await user.send(f'Remaining 🤏 vote 3h before event: **{title}** in {channel.mention} -> *adding point to leaderboard*')
        await asyncio.sleep(5)