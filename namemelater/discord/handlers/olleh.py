from namemelater.discord.handlers import OnMessage


class OllehWorld(OnMessage):
    priority = 0
    terminal = True

    async def condition(self, message):
        return message.content.startswith("!hello")

    async def on_message(self, message):
        await message.reply(message.content[::-1], mention_author=True)
