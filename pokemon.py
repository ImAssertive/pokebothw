import discord, asyncio, sys, traceback, checks, inflect, useful, random
from discord.ext import commands

class pokeCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, *, stopname):
        query = "SELECT * FROM Pokestops WHERE name = $1"
        result = await ctx.bot.db.fetchrow(query, stopname.lower())
        if not result:
            await ctx.channel.send(":no_entry: | No Pokestop with name:** "+stopname+"** found.")
        else:
            await ctx.channel.send("wew")

    @commands.command()
    @checks.justme()
    async def addstop(self, ctx):
        stoptype = "wew"
        await ctx.channel.send(":rotating_light: | Please enter the type of the stop.")
        def check(msg):
            options = ["gym", "pokestop", "stop"]
            return ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id and msg.content.lower() in options
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command window has closed due to inactivity. Please use the addstop command again to restart the proccess.")
        else:
            if msg.content.lower() == "gym":
                stoptype = "gym"
                print("made it to gym")
            elif msg.content.lower() == "pokestop" or msg.content.lower() == "stop":
                stoptype = "pokestop"
                print("made it to stop")
        if stoptype != "wew":
            print("do the rest of the program")
        else:
            print("timeout i think?")



        # stoptextlist = [[":rotating_light: | Please enter the name of the pokestop.", "name", ""],
        #                 [":rotating_light: | Please enter the url of the screenshot of the pokestop.", "screenshoturl", ""],
        #                 [":rotating_light: | Please enter the url of the map location of the pokestop.", "mapurl", ""],
        #                 [":rotating_light: | Please enter the url of the photo of the pokestop.", "imageurl", ""],
        #                 [":rotating_light: | Please enter the map coordanites of the pokestop.", "coord", ""]]


def setup(bot):
    bot.add_cog(pokeCog(bot))