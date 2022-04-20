from tortoise import models, fields


class Test(models.Model):
    id = fields.UUIDField(pk=True)
    file = fields.CharField(max_length=150)
    discipline = fields.ForeignKeyField(
        "models.Discipline",
        on_delete="SET NULL",
        null=True
    )
    competencies = fields.ManyToManyField(
        "models.Competence",
        on_delete="SET NULL",
        null=True
    )
