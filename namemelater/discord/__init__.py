import pkgutil

from interactions import Client, Intents, listen
from interactions.ext import prefixed_commands

from namemelater.discord.handlers import OnMessage


class NameMeLaterBot(Client):
    @listen()
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

    @listen()
    async def on_message_create(self, event):
        print(f"Message from {event.message.author}: {event.message.content}")
        # Our bot should not pay attention to its own messages
        if event.message.author.id == self.user.id:
            return

        for handler in self.handlers:
            if await handler.condition(event.message):
                await handler.on_message(event.message)
                if handler.terminal:
                    break


bot = NameMeLaterBot(
    description="I'm doing my part!",
    intents=Intents.ALL,
)

prefixed_commands.setup(bot, default_prefix="!")

for _, name, _ in pkgutil.walk_packages(
    [__path__[0] + "/commands"], prefix=__name__ + ".commands."
):
    bot.load_extension(name)
