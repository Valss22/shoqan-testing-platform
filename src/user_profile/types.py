from enum import Enum


class Courses(Enum):
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"
    FOURTH = "4"


class Specialties(Enum):
    ONE = "Корпоративные информационные системы"


class StressLevels(Enum):
    ONE = "очень низкий"
    TWO = "низкий"
    THREE = "ниже среднего"
    FOUR = "чуть ниже среднего"
    FIVE = "средний"
    SIX = "чуть выше среднего"
    SEVEN = "выше среднего"
    EIGHT = "высокий"
    NINE = "очень высокий"
