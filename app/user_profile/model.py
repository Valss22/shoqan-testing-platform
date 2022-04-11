from enum import Enum
from typing import Union

import bcrypt
from tortoise import models, fields

from app.settings import SALT


class UserProfile(models.Model):
    id = fields.UUIDField(pk=True)
    full_name = fields.CharField(max_length=150)
    university = fields.CharField(max_length=150)
