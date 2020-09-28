import discord
from discord.ext import commands
import praw
import random
import os
# from config import discord_config, reddit_config

# # For local testing only
# reddit = praw.Reddit(client_id=reddit_config["client_id"],
#                      client_secret=reddit_config["client_secret"],
#                      username=reddit_config["username"],
#                      password=reddit_config["password"],
#                      user_agent=reddit_config["user_agent"])
#
# TOKEN = discord_config["TOKEN"]

# actual config
# reddit config
reddit = praw.Reddit(client_id=os.environ["client_id"],
                     client_secret=os.environ["client_secret"],
                     username=os.environ["username"],
                     password=os.environ["password"],
                     user_agent="heroku")
# discord config
TOKEN = os.environ["TOKEN"]

client = commands.Bot(command_prefix="uwu ")

# removing the default "uwu help" command
client.remove_command("help")


def is_dupe(guild_id, post_id):
    combined_id = f"{guild_id}-{post_id}"
    with open("duplicates.txt", "r") as file:
        data = file.readlines()
        for line in data:
            if combined_id in line:
                return True
        return False

# TODO: uwu not Uwu
# # help user if they type Uwu/UwU... instead of uwu
# @client.event
# async def on_message(message):
#     print(f"{message.author}: {message.content}")
#     channel = message.channel
#     if message.content.startswith("Uwu" or "UwU" or "UWU" or "owo" or "Owo" or "OwO"):
#         await channel.send("use `uwu`")


# send a msg when the bot is ready and set status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("uwu help"))
    print("uwu!")


# show help text
@client.command(aliases=["commands", "Help"])
async def help(ctx):
    embed = discord.Embed()
    embed.set_author(name="Available Commands")
    embed.add_field(name="`uwu ping`", value="_", inline=False)
    embed.add_field(name="`uwu ques <your question here>`", value="_", inline=False)
    embed.add_field(name="`uwu clear <no. of msgs to delete>`", value="_", inline=False)
    embed.add_field(name="`uwu joke`", value="_", inline=False)
    embed.add_field(name="`uwu waifu`", value="_", inline=False)
    embed.add_field(name="`uwu animeart`", value="_", inline=False)
    embed.add_field(name="`uwu wallpaper`", value="_", inline=False)
    embed.add_field(name="`uwu meme`", value="_", inline=False)
    embed.add_field(name="`uwu codingmeme`", value="_", inline=False)
    # embed.add_field(name="`uwu hentai`", value="_", inline=False)
    embed.add_field(name="`uwu destiny`", value="_", inline=False)
    embed.add_field(name="`uwu pubg`", value="_", inline=False)
    embed.add_field(name="`uwu apex`", value="_", inline=False)
    embed.add_field(name="`uwu warzone`", value="_", inline=False)
    embed.add_field(name="`uwu amongus`", value="beta", inline=False)

    await ctx.send(embed=embed)


# get ping of the bot
@client.command(aliases=["latency"])
async def ping(ctx):
    await ctx.send(f"ping {round(client.latency * 1000)} ms uwu")


# 8ball (answers to a question randomly with yes/no/other shit)
@client.command(aliases=["8ball", "question"])
async def ques(ctx):
    response = ["yes uwu", "NO uwu", "why the F not? uwu", "ummm... idk lmao uwu", "ask that to your mom. uwu",
                "who cares uwu", "does it matter? uwu", "first look at yourself in the mirror you monke. uwu",
                "what kinda question is this you deep cabbage? uwu"]
    await ctx.send(f"{random.choice(response)}")


# deletes a certain number of recent msgs
@client.command(aliases=["clean", "delete"])
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


# uwu
@client.command(aliases=["Uwu", "UwU", "UWU"])
async def uwu(ctx):
    await ctx.send("uwu")


# [MAIN FUNCTIONALITY] posts a joke from r/jokes
@client.command(aliases=["jokes"])
async def joke(ctx):

    selected_posts = []

    try:
        for submission in reddit.subreddit("jokes").hot(limit=50):
            if not submission.stickied and submission.selftext:
                if not is_dupe(ctx.guild.id, submission.id):
                    selected_posts.append(submission)

        post = random.choice(selected_posts)

        guild_id = ctx.guild.id
        post_id = post.id

        with open("duplicates.txt", "a") as file:
            file.write(f"{guild_id}-{post_id}\n")

    except IndexError:
        for submission in reddit.subreddit("jokes").new(limit=50):
            if not submission.stickied and submission.selftext:
                selected_posts.append(submission)

        post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        description=post.selftext,
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts waifu pics uwu
@client.command(aliases=["anime"])
async def waifu(ctx):
    selected_posts = []
    subreddits = ["animeponytails", "awwnime", "streetmoe", "cutelittlefangs", "Gunime", "HimeCut",
                  "longhairedwaifus", "shorthairedwaifus", "twintails", "megane", "pouts", "Tsunderes", "ZettaiRyouiki"]

    for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=10):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.purple()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts waifu arts uwu
@client.command(aliases=["fan-art", "fanart", "art"])
async def animeart(ctx):
    selected_posts = []
    subreddits = ["Patchuu", "Pixiv"]

    for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=30):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.orange()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts wallpapers uwu
@client.command(aliases=["wallpapers"])
async def wallpaper(ctx):
    selected_posts = []
    subreddits = ["Animewallpaper", "Moescape", "wallpapers", "MinimalWallpaper", "EarthPorn"]

    for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=15):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blue()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts memes uwu
@client.command(aliases=["memes", "funny"])
async def meme(ctx):
    selected_posts = []
    subreddits = ["memes", "dankmemes", "me_irl", "wholesomememes"]

    for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=15):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blue()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts programming memes uwu
@client.command(aliases=["ProgrammerHumor", "programmingmeme", "codingmeme", "code"])
async def programming_meme(ctx):
    selected_posts = []
    subreddits = ["ProgrammerHumor", "ProgrammerAnimemes", "Recursion"]

    for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=20):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blue()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [NSFW][MAIN FUNCTIONALITY] posts hentai pics uwu
@client.command(aliases=["sex", "lewd", "nsfw", "ecchi", "nudes", "boobies", "porn"])
async def hentai(ctx):
    if ctx.channel.is_nsfw():
        selected_posts = []
        subreddits = ["hentai"]

        for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=50):
            if not submission.stickied:
                selected_posts.append(submission)
        post = random.choice(selected_posts)

        embed = discord.Embed(
            title=post.title,
            color=discord.Color.red()
        )
        embed.set_image(url=post.url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="jah dushtu! ( ͡° ͜ʖ ͡°)",
            description="Go to some NSFW channel or something.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts a destiny meme
@client.command(aliases=["destinymeme"])
async def destiny(ctx):
    selected_posts = []

    for submission in reddit.subreddit("DestinyMemes").hot(limit=20):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blurple()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts a PUBG meme
@client.command(aliases=["pubgay", "pubgmeme"])
async def pubg(ctx):
    selected_posts = []

    for submission in reddit.subreddit("PUBGmemes").hot(limit=20):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blurple()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts a apex legends meme
@client.command(aliases=["apexmeme", "apexlegends"])
async def apex(ctx):
    selected_posts = []

    for submission in reddit.subreddit("ApexOutlands").hot(limit=20):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blurple()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts a warzone meme
@client.command(aliases=["warzonememes", "warzonememe"])
async def warzone(ctx):
    selected_posts = []

    for submission in reddit.subreddit("warzonememes").hot(limit=20):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blurple()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# [MAIN FUNCTIONALITY] posts a among us meme
@client.command(aliases=["cursedamongus", "among_us", "among", "amongusmeme"])
async def amongus(ctx):
    selected_posts = []

    for submission in reddit.subreddit("cursedamongus").hot(limit=20):
        if not submission.stickied and not submission.over_18:
            selected_posts.append(submission)
    post = random.choice(selected_posts)

    embed = discord.Embed(
        title=post.title,
        color=discord.Color.blurple()
    )
    embed.set_image(url=post.url)
    await ctx.send(embed=embed)


# run the bot
client.run(TOKEN)
