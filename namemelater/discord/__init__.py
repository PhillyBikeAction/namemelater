import discord

from namemelater.discord.handlers import OnMessage


class NameMeLaterClient(discord.Client):
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


intents = discord.Intents.default()
intents.message_content = True

client = NameMeLaterClient(intents=intents)
