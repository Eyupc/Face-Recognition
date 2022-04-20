from datetime import datetime, date
class DateManager:
    __WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    def __init__(self):
        pass

    @classmethod
    def getTodayDayName(cls):
        return cls.__WEEKDAYS[date.today().weekday()]

