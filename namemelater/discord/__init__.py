import discord


class NameMeLaterClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        print(f"Joined guilds: {', '.join([str(g) for g in self.guilds])}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!hello"):
            await message.reply("Hello!", mention_author=True)


intents = discord.Intents.default()
intents.message_content = True

client = NameMeLaterClient(intents=intents)
