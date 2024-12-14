import click
from atproto import Client
import yaml

import os

with open('init.yaml', 'r') as file:
    credentials = yaml.safe_load(file)

usrname = credentials['login']['username']
password = credentials['login']['password']

__author__ = "charlotte"

@click.group()
def cli() -> None:
    """
    Simple CLI for logging into bluesky and seeing the first tweet in your timeline
    """

@cli.command()
def timeline():
    """
    Get posts from a user's timeline (chronological)
    """

    client = Client()
    client.login(usrname, password)

    timeline = client.get_timeline(algorithm='reverse-chronological')
    i = 0

    scrolling = True
    while scrolling:
        # current skeet (yes i am calling them skeets here lol)
        skeet = timeline.feed[i]

        
        post = skeet.post.record
        author = skeet.post.author
        likes = skeet.post.like_count
        reposts = skeet.post.repost_count
        replies = skeet.post.reply_count
        # skeet_date = skeet.record.created_at
        reason_for_skeet = skeet.reason

        # pretty print skeet info
        # click.secho(reason_for_skeet)
        click.secho(f'{author.display_name}  |   {post.created_at}', fg="blue")
        click.secho(f'{post.text}')
        click.secho(f'likes: {likes} | reposts: {reposts} | replies: {replies}', fg = "green")
    
        user_making_choice = True
        while user_making_choice:
            user_action = click.prompt("> ", default='n')

            # if tree for user actions
            if (user_action == 'n'):
                i = i + 1
                user_making_choice = False
            elif (user_action == 'b'):
                if i > 0:
                    i = i - 1
                    user_making_choice = False
                else:
                    click.echo("You're at the top of the feed. please refrench.")
            elif (user_action == 'm'):
                send_like(client, skeet.post)
            elif (user_action == 'v'):
                send_repost(client, skeet.post)
            elif (user_action == 'q'):
                user_making_choice = False
                scrolling = False
        
        click.clear()

@cli.command()
def init():
    """
    Setup user information if not already present
    """
    click.echo("You're good queen")
    
def send_like(client, post_to_like):
    client.like(uri=post_to_like.uri, cid=post_to_like.cid)

def send_repost(client, post_to_repost):
    client.repost(uri=post_to_repost.uri, cid=post_to_repost.cid)

if __name__ == "__main__":
    cli()