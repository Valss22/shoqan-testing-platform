from tortoise import models, fields

from src.discipline.types import Disciplines


class Discipline(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharEnumField(Disciplines)

