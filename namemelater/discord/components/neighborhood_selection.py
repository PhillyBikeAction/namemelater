import re

from interactions import (
    Button,
    ButtonStyle,
    Extension,
    component_callback,
    listen,
    spread_to_rows,
)
from interactions.api.events import Startup


class NeighborhoodSelection(Extension):
    # SELECTION_CHANNEL = 1194378656353624154

    # NEIGHBORHOODS = {
    #    "north": {
    #        "role_id": 1194379011896381602,
    #    },
    #    "south": {
    #        "role_id": 1194379082582982698,
    #    },
    #    "east": {
    #        "role_id": 1194379103965560903,
    #    },
    #    "west": {
    #        "role_id": 1194379120558219324,
    #    },
    #    "center_city": {
    #        "role_id": 1194379140795732018,
    #    },
    # }

    SELECTION_CHANNEL = 1174143043771842691

    NEIGHBORHOODS = {
        "north": {
            "role_id": 1193970494043594752,
        },
        "south": {
            "role_id": 1193970568475709610,
        },
        "west": {
            "role_id": 1193970678618140713,
        },
        "center_city": {
            "role_id": 1193970625224642640,
        },
        "east": {},
    }

    def __init__(self, bot):
        self.bot = bot
        BUTTONS = []
        for neighborhood_name, config in self.NEIGHBORHOODS.items():
            BUTTONS.append(
                Button(
                    style=ButtonStyle.PRIMARY,
                    label=neighborhood_name.replace("_", " ").capitalize(),
                    custom_id=f"neighborhood_selection_{neighborhood_name}",
                )
            )
        self.components = spread_to_rows(*BUTTONS)

    @listen(Startup)
    async def startup(self):
        await self.bot.get_channel(self.SELECTION_CHANNEL).send(
            "Select yer neighborhood!", components=self.components
        )

    BUTTON_ID_REGEX = re.compile(r"neighborhood_selection_(.*)")

    @component_callback(BUTTON_ID_REGEX)
    async def callback(self, ctx):
        neighborhood = ctx.custom_id.replace("neighborhood_selection_", "")
        if neighborhood == "east":
            await ctx.send("East? What are you, a fish?")
            return
        await ctx.member.add_roles([self.NEIGHBORHOODS[neighborhood]["role_id"]])
        await ctx.edit_origin(
            content="Select yer neighborhood!", components=self.components
        )


def setup(bot):
    NeighborhoodSelection(bot)
