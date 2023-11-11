import asyncio
import cmd
import os
import sys

import click
from discord.message import Message
import discord.ext.test as dpytest

from namemelater.cli import namemelater
from namemelater.discord import client as discord_client


class NameMeLaterShell(cmd.Cmd):
    intro = 'Welcome to the namemelater shell.\ntype `exit` or `Ctl-C` to exit.'
    prompt = '(namemelater) '
    file = None

    def __init__(self, *args, **kwargs):
        self.bot = discord_client
        self.loop = asyncio.get_event_loop()
        dpytest.configure(self.bot)
        super().__init__(*args, **kwargs)

    async def _message(self, content):
        await dpytest.message(content)
        response = await pdpytest.verify().message()._content
        print(response)

    def do_bot(self, arg):
        coroutine = self._message(arg)
        self.loop.run_until_complete(coroutine)

    def do_exit(self, arg):
        return True

    def precmd(self, line):
        if line.lower() != 'exit':
            return f"bot {line}"

@namemelater.command()
@click.pass_context
def dev(ctx):
    NameMeLaterShell().cmdloop()
