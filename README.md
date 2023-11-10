# NameMeLater

Philly Bike Action's Discord bot!

This codebase implements a set of interactions that can be initiated from the
discord server.

## Getting Started

### Docker

### Native

## Common activities

### Adding a dependency

This project uses [`pip-tools`](https://pip-tools.readthedocs.io/en/stable/)
to manage dependencies.

To add a dependency, you'll need to add the name (and any version specifiers)
to [`requirements.in`](requirements.in).

```
diff --git a/requirements.in b/requirements.in
index deadbee..fdeadbee 100644
--- a/requirements.in
+++ b/requirements.in
@@ -1,2 +1,3 @@
 discord.py
 pip-tools
+SomeProject == 5.4 ; python_version >= '3.11'
```

Then compile your dependencies and pin your hashes!

```
(venv) hostname:namemelater user$ pip-compile --generate-hashes
```

Commit the results and you're all set!

### Updating a dependency

Once compiled, the _only_ version allowed will be the one calculated at that time.

To update a specific package:

```
(venv) hostname:namemelater user$ pip-compile --generate-hashes -P SomePackage
```

To update _all_ dependencies:

```
(venv) hostname:namemelater user$ pip-compile --generate-hashes -U
```
