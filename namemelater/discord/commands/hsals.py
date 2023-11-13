from discord import Interaction, app_commands


@app_commands.command(name="hsals")
async def hsals(interaction: Interaction, number: int, string: str):
    await interaction.response.send_message(f"{number=} {string=}")
