import importlib
import pkgutil


class OnMessage:
    # defines the priority of this handler, lower numbers execute first
    # first condition to return true will have on_message called
    priority = 10

    # sets if this handler should stop all the rest from running
    terminal = True

    def __init__(self):
        ...

    async def condition(self, message):
        # Return True if condition for this handler is met
        ...

    async def on_message(self, message):
        # Do whatever you choose with the message!
        ...


# We want to automatically import all of the namemelater.discord.handlers.* modules so that
# any commands registered in any of them will be discovered.
for _, name, _ in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
    importlib.import_module(name)
