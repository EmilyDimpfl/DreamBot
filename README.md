# DreamBot
Discord bot for Patreon, to give folks roles after a certain amount of time with a role.

## Setup

In order to create a bot account to add to your server, follow the instructions at https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro

You can manage your bots on Discord's application developer page: https://discord.com/developers/applications

Once you have set up the bot, you'll want to add your discord bot token to your .env file.

Copy the `env.dev` file to `.env`, and change the `DISCORD_TOKEN=...` to `DISCORD_TOKEN=YOURTOKEN` (where `YOURTOKEN` is the token on the bot application page, obviously).

## Running

Run `dreambot.py`.

## Running in Docker

Run `docker-compose up -d`.
