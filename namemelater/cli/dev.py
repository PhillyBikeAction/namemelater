import os

import click

from namemelater.cli import namemelater
from namemelater.discord import bot


@namemelater.command()
@click.option(
    "--discord-token",
    default=lambda: os.environ.get("DISCORD_BOT_TOKEN", ""),
)
@click.option(
    "--db-url",
    default=lambda: os.environ.get("DATABASE_URL", ""),
)
def dev(discord_token, db_url):
    bot.load_extension("interactions.ext.jurigged", poll=True)
    bot.run(discord_token, db_url)
