import os

import click

from namemelater.cli import namemelater
from namemelater.discord import bot


@namemelater.command()
@click.option(
    "--discord-token",
    default=lambda: os.environ.get("DISCORD_BOT_TOKEN", ""),
)
def run(discord_token):
    bot.run(discord_token)
