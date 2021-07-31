import db
import json
import discord



def init_leaderboard():
    bot = db.bot
    guild_ID = db.guild_ID
    role_ID = db.leaderboard_role

    guild = bot.get_guild(id=guild_ID)
    for role in guild.roles:
        if role.id == role_ID:
            members = role.members
    
    leaderboard = {}
    for member in members:
        leaderboard[f'{member.display_name}'] = 0
    
    json.dump( leaderboard, open( "leaderboard.json", 'w' ) )

async def show_leaderboard(ctx):
    leaderboard = json.load( open( "leaderboard.json" ) )
    leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1], reverse=True))

    player_names = ''
    player_scores = ''
    for key, value in leaderboard.items():
        player_names += (key + '\n')
        player_scores += (str(value) + '\n')

    embed = discord.Embed(title='Leaderboard', color=0xFF9B00)
    embed.add_field(name='Player', value=player_names, inline=True)
    embed.add_field(name='Score', value=player_scores, inline=True)

    await ctx.channel.send(embed=embed)

async def add_point(members):
    leaderboard = json.load( open( "leaderboard.json" ) )

    for member in members:
        leaderboard[f'{member.display_name}'] += 1

    json.dump( leaderboard, open( "leaderboard.json", 'w' ) ) 

