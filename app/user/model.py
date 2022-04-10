import bcrypt
from tortoise import fields, models

from app.settings import SALT


class User(models.Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=128, unique=True)
    password_hash = fields.BinaryField()

    async def save(self, *args, **kwargs):
        self.password_hash = bcrypt.hashpw(self.password_hash, SALT)
        await super().save(*args, **kwargs)
