from discord import Interaction, app_commands


@app_commands.command(name="slash")
async def slash(interaction: Interaction, number: int, string: str):
    await interaction.response.send_message(f"{number=} {string=}", ephemeral=True)
