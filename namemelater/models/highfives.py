from tortoise.models import Model
from tortoise import fields


class HighFive(Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=64)
    high_fives = fields.IntField()

    def __str__(self):
        return f"{self.username}: 🫸{self.high_fives}🫷"
