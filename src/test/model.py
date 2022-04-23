from tortoise import models, fields

from src.test.validators import validate_range_number


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
    users = fields.ManyToManyField(
        "models.User",
        on_delete="SET NULL",
        null=True,
        through="models.UserToTest"
    )


class UserToTest(models.Model):
    user = fields.ForeignKeyField(
        "models.User",
        on_delete="SET NULL",
        null=True
    )
    test = fields.ForeignKeyField(
        "models.Test",
        on_delete="SET NULL",
        null=True
    )
    score = fields.SmallIntField(
        validators=[validate_range_number],
        null=True
    )
    passed = fields.BooleanField(null=True)
