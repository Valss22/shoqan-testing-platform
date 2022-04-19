from tortoise import models, fields


class Test(models.Model):
    id = fields.UUIDField(pk=True)
    file = fields.CharField(max_length=150)
