#!/usr/bin/env python3

import logging
import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from userdata import UserData

# Configure logging for both logging to a file and logging to stdout.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("dreambot.log"),
        logging.StreamHandler()
    ]
)

# per https://stackoverflow.com/a/73821983:
# > Since discord.py 2.0, you must now activate privleged intents for
# >  specific actions. Messages are one of those actions.
intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)  # create our client

load_dotenv()  # load our .env file into environment variables

data = UserData('dreamers.json')
dreamer_role_id = None
patron_role_id = None
scan_channel = None
promotion_time = None
scan_time = int(os.getenv('SCAN_TIME', 1440))  # default to once a day

@client.event
async def on_ready():
    """
    event when we log in
    """
    logging.info('We have logged in as {0.user}'.format(client))
    scan.start()


@tasks.loop(minutes=scan_time)
async def scan():
    # our effectively-static settings:
    global scan_channel
    global dreamer_role_id
    global patron_role_id
    global promotion_time
    global data
    global scan_time

    logging.debug(f"Channel ID: {scan_channel}")
    channel = client.get_channel(scan_channel)

    if channel is None:
        logging.debug("Unable to get channel.")
        return

    members = channel.members  # gets members in the channel

    for member in members:
        if dreamer_role_id in [r.id for r in member.roles]:
            logging.debug(f"Member {member.display_name} is Dreamer, skipping.")
            continue
        if patron_role_id in [r.id for r in member.roles]:
            logging.debug(f"Member {member.display_name} is Patron, adding time...")
            data.modify_user(member.id, scan_time)

            time = data.get_user_time(member.id)
            logging.debug(f"Member {member.display_name} has {time} time as a patron.")
            if time >= promotion_time:
                # promote user
                logging.info(f"Promoting user {member.display_name} ({member.id})")
                dreamer_role = member.guild.get_role(dreamer_role_id)

                await member.add_roles(dreamer_role)
        # (ignore non-patron users)
    logging.debug("Saving user data...")
    data.save_data(data.filepath)


def main():
    """
    runs our bot
    """
    # this is used to read our DISCORD_TOKEN in without having
    # the token committed to the repository.

    # Here's how you make a bot:
    # https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro

    # Here's discord.py's quick start:
    # https://discordpy.readthedocs.io/en/stable/quickstart.html

    # Here's discord.py's documentation:
    # https://discordpy.readthedocs.io/en/stable/index.html

    global dreamer_role_id
    global patron_role_id
    global scan_channel
    global promotion_time
    dreamer_role_id = int(os.environ['DREAMER_ROLE_ID'])
    patron_role_id = int(os.environ['PATRON_ROLE_ID'])
    scan_channel = int(os.environ['SCAN_CHANNEL'])
    promotion_time = int(os.environ['PROMOTION_TIME'])
    logging.debug(f'Veteran role id: {dreamer_role_id}')
    logging.debug(f'Patron role id: {patron_role_id}')
    logging.debug(f'Channel id: {scan_channel}')
    logging.debug(f'Promotion time: {promotion_time}')
    logging.debug(f'Scan time: {scan_time}')

    # run the client:
    client.run(os.environ['DISCORD_TOKEN'])
    # this blocks until we press Ctrl-C


if __name__ == "__main__":
    main()
