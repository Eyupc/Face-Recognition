from datetime import date


class DateManager:
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self):
        pass

    @classmethod
    def getTodayDayName(cls):
        return cls.WEEKDAYS[date.today().weekday()]
