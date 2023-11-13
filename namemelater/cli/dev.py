import os

import click

from namemelater.cli import namemelater
from namemelater.discord import bot


@namemelater.command()
@click.option(
    "--discord-token",
    default=lambda: os.environ.get("DISCORD_BOT_TOKEN", ""),
)
def dev(discord_token):
    bot.load_extension("interactions.ext.jurigged", poll=True)
    bot.start(discord_token)
