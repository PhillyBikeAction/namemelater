from interactions import (
    Extension,
    OptionType,
    SlashContext,
    slash_command,
    slash_option,
)


class HsalsCommand(Extension):
    @slash_command(name="hsals")
    @slash_option(
        name="integer_option",
        description="Integer Option",
        required=True,
        opt_type=OptionType.INTEGER,
    )
    @slash_option(
        name="string_option",
        description="String Option",
        required=True,
        opt_type=OptionType.STRING,
    )
    async def hsals(self, ctx: SlashContext, integer_option: int, string_option: str):
        await ctx.send(f"{integer_option=} {string_option=}")


def setup(bot):
    HsalsCommand(bot)
