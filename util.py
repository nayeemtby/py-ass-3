from datetime import datetime


def describeDateTime(time: datetime) -> str:
    return f'{time.year}/{time.month}/{time.day} {time.hour}:{time.minute}:{time.second}'
