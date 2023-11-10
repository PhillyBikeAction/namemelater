import os

import click

from namemelater.cli import namemelater
from namemelater.discord import client as discord_client


@namemelater.command()
@click.option(
    "--discord-token",
    default=lambda: os.environ.get("DISCORD_BOT_TOKEN", ""),
)
def run(discord_token):
    discord_client.run(discord_token)
