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
            await ctx.channel.send(":no_entry: | No Pokestop with name:** "+stopname.lower()+"** found.")
        else:
            embed = discord.Embed(title="Menu Loading...", description="Please stand by.", colour=self.bot.getcolour())
            menu = await ctx.channel.send(embed = embed)
            emojis = useful.getInfoMenuEmoji()
            for emoji in range(0,len(emojis)):
                await menu.add_reaction(emojis[emoji])
            await self.infoMainMenu(ctx, menu, result)

    async def infoMainMenu(self, ctx, menu, result):
            embed = discord.Embed(description="Use the reactions to navigate the menu.", colour=self.bot.getcolour())
            embed.add_field(name=result["type"].title()+" name:", value=result["name"])
            embed.add_field(name=result["type"].title()+" coordinates:", value=result["coord"])
            embed.add_field(name=result["type"].title()+" notes:", value=result["notes"], inline=False)
            embed.set_footer(text="Page (1/4)")
            embed.set_author(icon_url="https://i.imgur.com/eXKzHVr.jpg",name="Here is the information for stop: "+result["name"])
            await menu.edit(embed=embed)
            options = useful.getInfoMenuEmoji()
            def info_emojis_main_menu(reaction, user):
                return (user == ctx.author) and (str(reaction.emoji) in options)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=info_emojis_main_menu, timeout=60.0)
            except asyncio.TimeoutError:
                ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command menu has closed due to inactivity.")
                await menu.delete()
            else:
                await menu.remove_reaction(reaction.emoji, user)
                if str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenu(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenuPage4(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenuPage2(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenuPage4(ctx, menu, result)
                elif str(reaction.emoji) == "❌":
                    closed = await ctx.channel.send(":white_check_mark: | Info closed!")
                    await menu.delete()
                    await asyncio.sleep(1)
                    await closed.delete()

    async def infoMainMenuPage2(self, ctx, menu, result):
            embed = discord.Embed(description="Use the reactions to navigate the menu.", colour=self.bot.getcolour())
            print(result["screenshoturl"])
            embed.set_image(url=result["screenshoturl"])
            embed.set_footer(text="Page (2/4)")
            embed.set_author(icon_url="https://i.imgur.com/eXKzHVr.jpg",name="Screenshot of: "+result["name"])
            await menu.edit(embed=embed)
            options = useful.getInfoMenuEmoji()
            def info_emojis_main_menu(reaction, user):
                return (user == ctx.author) and (str(reaction.emoji) in options)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=info_emojis_main_menu, timeout=60.0)
            except asyncio.TimeoutError:
                ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command menu has closed due to inactivity.")
                await menu.delete()
            else:
                await menu.remove_reaction(reaction.emoji, user)
                if str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenu(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenu(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenuPage3(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenuPage4(ctx, menu, result)
                elif str(reaction.emoji) == "❌":
                    closed = await ctx.channel.send(":white_check_mark: | Info closed!")
                    await menu.delete()
                    await asyncio.sleep(1)
                    await closed.delete()

    async def infoMainMenuPage3(self, ctx, menu, result):
            embed = discord.Embed(description="Use the reactions to navigate the menu.", colour=self.bot.getcolour())
            embed.set_image(url=result["mapurl"])
            embed.set_footer(text="Page (3/4)")
            embed.set_author(icon_url="https://i.imgur.com/eXKzHVr.jpg",name="Map location of: "+result["name"])
            await menu.edit(embed=embed)
            options = useful.getInfoMenuEmoji()
            def info_emojis_main_menu(reaction, user):
                return (user == ctx.author) and (str(reaction.emoji) in options)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=info_emojis_main_menu, timeout=60.0)
            except asyncio.TimeoutError:
                ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command menu has closed due to inactivity.")
                await menu.delete()
            else:
                await menu.remove_reaction(reaction.emoji, user)
                if str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenu(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenuPage2(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenuPage4(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenuPage4(ctx, menu, result)
                elif str(reaction.emoji) == "❌":
                    closed = await ctx.channel.send(":white_check_mark: | Info closed!")
                    await menu.delete()
                    await asyncio.sleep(1)
                    await closed.delete()

    async def infoMainMenuPage4(self, ctx, menu, result):
            embed = discord.Embed(description="Use the reactions to navigate the menu.", colour=self.bot.getcolour())
            embed.set_image(url=result["imageurl"])
            embed.set_footer(text="Page (4/4)")
            embed.set_author(icon_url="https://i.imgur.com/eXKzHVr.jpg",name="Picture of stop: "+result["name"])
            await menu.edit(embed=embed)
            options = useful.getInfoMenuEmoji()
            def info_emojis_main_menu(reaction, user):
                return (user == ctx.author) and (str(reaction.emoji) in options)
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=info_emojis_main_menu, timeout=60.0)
            except asyncio.TimeoutError:
                ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command menu has closed due to inactivity.")
                await menu.delete()
            else:
                await menu.remove_reaction(reaction.emoji, user)
                if str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenu(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenuPage3(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}":
                    await self.infoMainMenu(ctx, menu, result)
                elif str(reaction.emoji) == "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}":
                    await self.infoMainMenuPage4(ctx, menu, result)
                elif str(reaction.emoji) == "❌":
                    closed = await ctx.channel.send(":white_check_mark: | Info closed!")
                    await menu.delete()
                    await asyncio.sleep(1)
                    await closed.delete()

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
            elif msg.content.lower() == "pokestop" or msg.content.lower() == "stop":
                stoptype = "pokestop"
        if stoptype != "wew":
            timeout = False
            stoptextlist = [[":rotating_light: | Please enter the name of the "+stoptype+".", "name", "", "pokestop name"],
                            [":rotating_light: | Please enter the url of the screenshot of the "+stoptype+".", "screenshoturl", "", "screenshot url"],
                            [":rotating_light: | Please enter the url of the map location of the "+stoptype+".", "mapurl", "", "map location url"],
                            [":rotating_light: | Please enter the url of the photo of the "+stoptype+".", "imageurl", "", "photo url"],
                            [":rotating_light: | Please enter the map coordanites of the "+stoptype+".", "coord", "", "map coordinates"],
                            [":rotating_light: | Please enter any additional notes for this "+stoptype+".", "notes", "", "notes"]]
            for option in stoptextlist:
                await ctx.channel.send(option[0])
                def check(msg):
                    return ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    timeout = True
                    await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command window has closed due to inactivity. Please use the addstop command again to restart the proccess.")
                else:
                    if "://" in msg.content:
                        print("wew")
                        option[2] = msg.content
                    else:
                        option[2] = msg.content.lower()
            if not timeout:
                embed = discord.Embed(description="Please type confirm to confirm adding to database or cancel to discard.", colour=self.bot.getcolour())
                embed.set_author(icon_url="https://i.imgur.com/eXKzHVr.jpg", name="Here is the information for "+stoptype+": "+stoptextlist[0][2]+".")
                embed.add_field(name=stoptype+" name:", value=stoptextlist[0][2], inline=False)
                embed.add_field(name=stoptype+" screenshot url:", value=stoptextlist[1][2], inline=False)
                embed.add_field(name=stoptype+" map location url:", value=stoptextlist[2][2], inline=False)
                embed.add_field(name=stoptype+" photo url:", value=stoptextlist[3][2], inline=False)
                embed.add_field(name=stoptype+" map coordanites", value=stoptextlist[4][2], inline=False)
                embed.add_field(name=stoptype+" notes", value=stoptextlist[5][2], inline=False)
                embed.set_footer(text="bot made by Zootopia#0001")
                await ctx.channel.send(embed=embed)
                def check(msg):
                    options = ["cancel", "confirm"]
                    return ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id and msg.content.lower() in options
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=60.0)
                except asyncio.TimeoutError:
                    await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The command window has closed due to inactivity. Please use the addstop command again to restart the proccess.")
                else:
                    if msg.content.lower() == "cancel":
                        await ctx.channel.send(":white_check_mark: | "+stoptype.title()+" discarded!")
                    elif msg.content.lower() == "confirm":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "INSERT INTO Pokestops (name, screenshoturl, mapurl, imageurl, coord, type, notes) VALUES($1, $2, $3, $4, $5, $6, $7) ON CONFLICT DO NOTHING"
                            await self.bot.db.execute(query, stoptextlist[0][2], stoptextlist[1][2], stoptextlist[2][2], stoptextlist[3][2], stoptextlist[4][2], stoptype, stoptextlist[5][2])
                        await self.bot.db.release(connection)
                        await ctx.channel.send(":white_check_mark: | "+stoptype.title()+" added!")


def setup(bot):
    bot.add_cog(pokeCog(bot))