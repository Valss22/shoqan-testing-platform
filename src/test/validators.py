from tortoise.exceptions import ValidationError


def validate_range_score(value: int):
    if value not in range(31):
        raise ValidationError(f"Value '{value}' must be in range from 0 to 30")
