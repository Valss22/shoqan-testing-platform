from tortoise import models, fields

from src.user_profile.types import Courses, Specialties, StressLevels


class UserProfile(models.Model):
    id = fields.UUIDField(pk=True)
    fullname = fields.CharField(max_length=150)
    specialty = fields.CharEnumField(Specialties)
    course = fields.CharEnumField(Courses)
    photo = fields.CharField(max_length=150)
    stress = fields.CharEnumField(StressLevels, null=True)
