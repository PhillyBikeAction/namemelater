import gc
import importlib
import pkgutil

import discord
from discord.ext import commands as discord_commands

from namemelater.discord.handlers import OnMessage


class NameMeLaterBot(discord_commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        print(f"Joined guilds: {', '.join([str(g) for g in self.guilds])}")

        self.handlers = [
            handler()
            for handler in sorted(OnMessage.__subclasses__(), key=lambda x: x.priority)
        ]
        print("Loaded handlers:")
        for handler in self.handlers:
            print(handler.priority, handler)

        print("Loaded commands:")
        for c in self.commands:
            print(c)

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        # Our bot should not pay attention to its own messages
        if message.author.id == self.user.id:
            return

        for handler in self.handlers:
            if await handler.condition(message):
                await handler.on_message(message)
                if handler.terminal:
                    break

        await self.process_commands(message)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = NameMeLaterBot(
    command_prefix="!",
    description="I'm doing my part!",
    intents=intents,
)

existing = []
for obj in gc.get_objects():
    if isinstance(obj, discord_commands.Command):
        existing.append(obj)

# We want to automatically import all of the namemelater.discord.commands.* modules so that
# any commands registered in any of them will be discovered.
for _, name, _ in pkgutil.walk_packages(
    [__path__[0] + "/commands"], prefix=__name__ + ".commands."
):
    importlib.import_module(name)

for obj in gc.get_objects():
    if isinstance(obj, discord_commands.Command) and obj not in existing:
        bot.add_command(obj)
