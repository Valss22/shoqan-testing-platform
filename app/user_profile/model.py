# import bcrypt
# from tortoise import models, fields
#
# from app.settings import SALT
#
#
# class UserProfile(models.Model):
#     id = fields.UUIDField(pk=True)
#     email = fields.CharField(max_length=128, unique=True)
#     password_hash = fields.BinaryField()
#
#     async def save(self, *args, **kwargs):
#         self.password_hash = bcrypt.hashpw(self.password_hash, SALT)
#         await super().save(*args, **kwargs)


a = [{'a': 1, 'p': 2}]

b = {'a': 21, 'p': 22}

if b in a:
    print('yes')