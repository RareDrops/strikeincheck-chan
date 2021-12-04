from json.decoder import JSONDecodeError
from logging import info
import discord
from discord.ext import commands, tasks
import json
import datetime

# step by step procedure: (how the bot works)
# 1. the bot forms a dictionary(a) of ppl with a specific role. Their user ID being the key and name being the value.
# 2. the bot then forms another dictionary(b) from the reaction of the message. The emoji name being the key, the list of users being the value.
# 3. the bot then iterates through the keys of dictionary(b), getting the value(list) then converts it to a set.
# 4. the bot uses python set operation(difference): dictionary(a)/dictionary(b) to find the keys on dictionary(a) that's not on dictionary(b).
# 5. the bot displays the value of the remaining keys(their names)

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)
client.remove_command('help')

#event actions
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#commands
@client.command()
async def get_reactions(ctx, message_id):
    #fetching the members with a specific role
    try:
        with open("priconne_data.json",'r') as in_file:
            data = json.load(in_file)
            in_file.close()
    except (KeyError, FileNotFoundError):
        await ctx.send("Set the clan role first by using !set_role command, check !help for the documentation.")
    except discord.NotFound:
        await ctx.send("The argument is not a message id.")

    guild = ctx.guild
    channel = guild.get_channel(data[str(guild.id)]["channel"])
    role = guild.get_role(data[str(guild.id)]["role"])
    member_list = role.members
    member_dictionary = {member.id:member.name for member in member_list}

    #fetching the members that reacted to a specific message by the message id
    message = await channel.fetch_message(message_id)
    for reaction in message.reactions:
        reaction_user_list = await reaction.users().flatten()
        reaction_user_dictionary = {member.id:member.name for member in reaction_user_list}
        missing_members = member_dictionary.keys() - reaction_user_dictionary.keys() #converts the dictionary into a set-like object using the keys then find the difference
        word_list = f"{reaction}\n" #just turns the entire list into a formatted string
        for i, member in enumerate(missing_members):
            word_list += f"{str(i+1)}. {str(member_dictionary[member])} \n"
        await ctx.send(word_list)
    

@client.command()
async def set_role(ctx, role):
    try:
        role = int(role)
    except ValueError:
        await ctx.send("You need to put a role id as the argument. To get the role id, you need to have developer options enabled and right click the role then copy id. Example: !set_role 378216273513297321")
    guild = ctx.guild.id
    #checks if the json file is empty or can't be found, exception will be raised and altenative solution will take action
    try:
        with open("priconne_data.json",'r') as in_file:
            data = json.load(in_file)
            in_file.close()
        data[str(ctx.guild.id)]["role"] = role
        guild_role_dict = data
    except (FileNotFoundError, JSONDecodeError):
        guild_role_dict = {guild:{"role":role}}
    with open("priconne_data.json",'w') as out_file:
        json.dump(guild_role_dict,out_file,indent=4)
        out_file.close()
    await ctx.send("Successfully sets the clan role.")

@client.command()
async def set_channel(ctx, channel):
    try:
        channel = int(channel)
    except ValueError:
         await ctx.send("You need to put a channel id as the argument. To get the channel id, you need to have developer options enabled and right click the channel then copy id. Example: !set_channel 378216273513297321")
    guild = ctx.guild.id
    #checks if the json file is empty or can't be found, exception will be raised and altenative solution will take action
    try:
        with open("priconne_data.json",'r') as in_file:
            data = json.load(in_file)
            in_file.close()
        data[str(ctx.guild.id)]["channel"] = channel
        guild_channel_dict = data
    except (FileNotFoundError, JSONDecodeError):
        guild_channel_dict = {guild:{"channel":channel}}
    with open("priconne_data.json",'w') as out_file:
        json.dump(guild_channel_dict,out_file,indent=4)
        out_file.close()
    await ctx.send(f"Successfully sets the strike-in channel to <#{channel}>.")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help Center!",
                            color=discord.Color.random(),
                            timestamp=datetime.datetime.utcnow())
    embed.add_field(
            name="!set_role [role id]",
            value="Sets your clan's role. Example: !set_role 987312632817318312",
            inline=False)
    embed.add_field(
            name="!set_channel [channel id]",
            value="Set the channel strike-ins. Example: !set_channel 2727321987312612136",
            inline=False)
    embed.add_field(
            name="!get_reactions [message id]",
            value="Displays the clan members that didn't react to the message. Example: !get_reactions 783216216339721312",
            inline=False)
    embed.set_thumbnail(
            url="https://media.socastsrm.com/wordpress/wp-content/blogs.dir/460/files/2016/04/tumblr_ni7bjoVEZu1qefok0o2_500.gif"
        )
    embed.set_image(url="https://i.imgur.com/xnpRxfV.gif")
    embed.set_footer(
        text=ctx.guild.name,
        icon_url=f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{ctx.guild.icon}.webp"
    )
    await ctx.channel.send(embed=embed)
    





client.run("PUT YOUR TOKEN HERE")
