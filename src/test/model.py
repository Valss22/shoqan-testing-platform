from tortoise import models, fields

from src.test.validators import validate_range_score


class Test(models.Model):
    id = fields.UUIDField(pk=True)
    file = fields.CharField(max_length=150)
    filename = fields.CharField(max_length=150)
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
        through="user_to_test"
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
        validators=[validate_range_score],
        null=True
    )
    passed = fields.BooleanField(null=True)

    attempts = fields.SmallIntField(default=0)  # TODO поставить валидацию

    class Meta:
        table = "user_to_test"
