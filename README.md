# NameMeLater

Philly Bike Action's Discord bot!

This codebase implements a set of interactions that can be initiated from the
discord server.

It is built with interactions-py [docs](https://interactions-py.github.io/interactions.py/Guides/).

## Getting Started

You will need a Discord bot token to _actually_ run the bot.

The best way is to setup your own guild for testing/development and then
follow the excellent guide on [Creating a Bot](https://interactionspy.readthedocs.io/en/latest/quickstart.html#creating-a-bot)
from interactions-py's documentation.

```shell
echo 'DISCORD_BOT_TOKEN="PBA..replace with your token..BL4A"' > .env
```

TODO: A development mode is provided that just drops you into a REPL with
`namemelater`.

### Docker

```
docker compose run --rm namemelater
```

This will start the bot and auto-reload it anytime code changes!

### Native

```shell
python3.11 -m venv venv
source venv/bin/activate
source .env
pip install -r requirements.txt
python -m namemelater dev
```

This will start the bot and hot-reload it anytime code changes!

## Common activities

### Adding a command

Commands can be added by creating an interaction-py
[Extension](https://interactions-py.github.io/interactions.py/Guides/20%20Extensions/)
[`namemelater/discord/commands`](namemelater/discord/commands).

Please see interactions-py's
[documentation](https://interactions-py.github.io/interactions.py/Guides/03%20Creating%20Commands/)
on commands!

### Adding a message handler

Message handlers are created by adding a module to
[`namemelater/discord/handlers`](namemelater/discord/handlers).

That module should contain a class that inherits from
[`OnMessage`](namemelater/discord/handlers/__init__.py)
and implements both a `condition` and `on_message` method.

`condition` is called with a interactions-py `event.message` object and determines
if the handler will be called. If `condition` returns `True`, `on_message`
will be called with the same `Message` object.

Handlers can set `priority` and `terminal` attributes that configure
what order they well be checked in (lower `priority` values execute first)
and if once `on_message` is called the execution should cease (basically no
more handlers will be checked or executed if `terminal = True`.

### Adding a dependency

This project uses [`pip-tools`](https://pip-tools.readthedocs.io/en/stable/)
to manage dependencies.

To add a dependency, you'll need to add the name (and any version specifiers)
to [`requirements/main.in`](requirements/main.in).

```
diff --git a/requirements/main.in b/requirements/main.in
index deadbee..fdeadbee 100644
--- a/requirements/main.in
+++ b/requirements/main.in
@@ -1,2 +1,3 @@
 discord.py
 pip-tools
+SomeProject == 5.4 ; python_version >= '3.11'
```

Then compile your dependencies and pin your hashes!

```
(venv) hostname:namemelater user$ pip-compile --generate-hashes requirements/main.in
```

Commit the results and you're all set!

### Updating a dependency

Once compiled, the _only_ version allowed will be the one calculated at that time.

To update a specific package:

```
(venv) hostname:namemelater user$ pip-compile --generate-hashes requirements/main.in -P SomePackage
```

To update _all_ dependencies:

```
(venv) hostname:namemelater user$ pip-compile --generate-hashes requirements/main.in -U
```
