from namemelater.discord.handlers import OnMessage


class HelloWorld(OnMessage):
    priority = 10
    terminal = True

    async def condition(self, message):
        return message.content.startswith("!hello")

    async def on_message(self, message):
        await message.reply("Hello!", mention_author=True)
