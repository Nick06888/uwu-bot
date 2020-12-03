import random
import discord


def is_dupe(guild_id, post_id):
    combined_id = f"{guild_id}-{post_id}"
    with open("duplicates.txt", "r") as file:
        data = file.readlines()
        for line in data:
            if combined_id in line:
                return True
        return False


def clear_dupes(file_name):
    with open(file_name, "w") as file:
        file.write("")


def select_post(ctx, reddit, subreddits, selected_posts, limit=50):
    try:
        for submission in reddit.subreddit(random.choice(subreddits)).hot(limit=limit):
            if not submission.stickied and not submission.over_18:
                if not is_dupe(ctx.guild.id, submission.id):
                    selected_posts.append(submission)

        selected_post = random.choice(selected_posts)

        guild_id = ctx.guild.id
        post_id = selected_post.id

        with open("duplicates.txt", "a") as file:
            file.write(f"{guild_id}-{post_id}\n")

    except IndexError:
        for submission in reddit.subreddit(random.choice(subreddits)).new(limit=limit):
            if not submission.stickied and not submission.over_18:
                selected_posts.append(submission)

        selected_post = random.choice(selected_posts)

    return selected_post


def prepare_embed(ctx, post, color=discord.Color.blue()):
    embed = discord.Embed(
        title=post.title,
        color=color
    )
    embed.set_image(url=post.url)
    return embed

