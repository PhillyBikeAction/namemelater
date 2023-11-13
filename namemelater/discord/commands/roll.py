import random

from interactions import Extension
from interactions.ext.prefixed_commands import prefixed_command, PrefixedContext


class RollCommand(Extension):
    @prefixed_command(name="roll")
    async def roll(self, ctx: PrefixedContext, dice: str = None):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split("d"))
        except Exception:
            await ctx.reply("Format has to be in NdN!")
            return

        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.reply(result)


def setup(bot):
    RollCommand(bot)
