from tortoise import models, fields

from src.competence.types import Competencies


class Competence(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharEnumField(Competencies)
    disciplinies = fields.ManyToManyField(
        "models.Discipline",
        on_delete="SET NULL",
        null=True
    )
    owners = fields.ManyToManyField(
        "models.User",
        on_delete="SET NULL",
        null=True
    )
