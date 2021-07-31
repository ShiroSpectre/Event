from discord.ext import commands
from functions import create_event, leaderboard_func, list_events

class Calendar(commands.Cog):
    """All commands about the calendar functionality"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='Heute 18:00 / .event Fr 18 Uhr / .event 12.12. 18:00 Primeleague')
    async def event(self, ctx, *args):
        """Creation of a calendar event"""
        await ctx.message.delete()
        await create_event.create(ctx, args)
    
    @commands.command(usage='')
    async def upcoming(self, ctx):
        """Lists all upcoming events"""
        await list_events.list_all_events(ctx)
        await ctx.message.delete()

    @commands.command(usage='')
    async def leaderboard(self, ctx):
        """Show the TOP 10 Challenger Ladder"""
        await ctx.message.delete()
        await leaderboard_func.show_leaderboard(ctx)

def setup(bot):
    bot.add_cog(Calendar(bot))