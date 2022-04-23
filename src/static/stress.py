from src.user_profile.types import StressLevels

SELDOM = "редко"
SOMETIMES = "иногда"
OFTEN = "часто"

answers = [SELDOM, SOMETIMES, OFTEN]

answer_scores: dict[str, int] = {
    SELDOM: 1,
    SOMETIMES: 2,
    OFTEN: 3
}

stress_lvl: dict[StressLevels, range] = {
    StressLevels.ONE: range(50, 54),
    StressLevels.TWO: range(46, 50),
    StressLevels.THREE: range(42, 46),
    StressLevels.FOUR: range(38, 42),
    StressLevels.FIVE: range(34, 38),
    StressLevels.SIX: range(30, 34),
    StressLevels.SEVEN: range(26, 30),
    StressLevels.EIGHT: range(22, 26),
    StressLevels.NINE: range(18, 22),
}

stress_obj: list[dict] = [
    {
        "question": "Я думаю, что меня недооценивают в коллективе",
        "answers": answers
    },
    {
        "question": "Я стараюсь работать, даже если бываю не совсем здоров",
        "answers": answers
    },
    {
        "question": "Я постоянно переживаю за качество своей работы",
        "answers": answers
    },
    {
        "question": "Я бываю настроен агрессивно",
        "answers": answers
    },
    {
        "question": "Я не терплю критики в свой адрес",
        "answers": answers
    },
    {
        "question": "Я бываю раздражителен",
        "answers": answers
    },
    {
        "question": "Я стараюсь быть лидером там, где это возможно",
        "answers": answers
    },
    {
        "question": "Меня считают человеком настойчивым и напористым",
        "answers": answers
    },
    {
        "question": "Я страдаю бессоницей",
        "answers": answers
    },
    {
        "question": "Своим недругам я могу дать отпор",
        "answers": answers
    },
    {
        "question": "Я эмоционально и болезненно переживаю неприятность",
        "answers": answers
    },
    {
        "question": "У меня не хватает времени на отдых",
        "answers": answers
    },
    {
        "question": "У меня возникают конфликтные ситуации",
        "answers": answers
    },
    {
        "question": "Мне недостает власти, чтобы реализовать себя",
        "answers": answers
    },
    {
        "question": "У меня не хватает времени, чтобы заняться любимым делом",
        "answers": answers
    },
    {
        "question": "Я все делаю быстро",
        "answers": answers
    },
    {
        "question": "Я испытываю страх, что потеряю работу(или не поступлю в институт)",
        "answers": answers
    },
    {
        "question": "Я действую сгоряча, а затем переживаю за свои дела и поступки",
        "answers": answers
    },
]
