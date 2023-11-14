import os

db_url = os.environ.get("DATABASE_URL", "asyncpg://postgres@db/postgres")

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "namemelater": {
            "models": ["namemelater.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
