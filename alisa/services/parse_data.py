from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from schemas.alice_request import AliceRequest

weekday_dict = {
    1: "понедельник",
    2: "вторник",
    3: "среда",
    4: "четверг",
    5: "пятница",
    6: "суббота",
    7: "воскресенье",
}

month_numbers = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
}

def get_day_by_timeword(word):
    now = datetime.now(tz=ZoneInfo("Europe/Moscow"))
    target_date = now.isoweekday()
    
    if word == 'позавчера': 
        target_date -= 2
    elif word == 'вчера':
        target_date -= 1
    elif word == 'завтра':
        target_date += 1
    elif word == 'послезавтра':
        target_date += 2
    
    if target_date < 1:
        target_date += 7
    elif target_date > 7:
        target_date -= 7
    
    return weekday_dict[target_date]

def normalize_day_name(day):
    day_mapping = {
        'понедельник': 'понедельник',
        'вторник': 'вторник',
        'среду': 'среда', 
        'среда': 'среда',
        'четверг': 'четверг',
        'пятницу': 'пятница',
        'пятница': 'пятница',
        'субботу': 'суббота',
        'суббота': 'суббота',
        'воскресенье': 'воскресенье'
    }
    return day_mapping.get(day.lower(), day)

def parse_date(alice_request: AliceRequest):
    today = datetime.now(tz=ZoneInfo("Europe/Moscow")).date()
    alice_request = AliceRequest.model_validate(alice_request)
    
    for entity in alice_request.request.nlu.entities:
        if entity.type == "YANDEX.DATETIME":
            value = entity.value
            if value.get('day_is_relative') and type(value.get('day')) == int:
                return today + timedelta(days=value['day'])
            try:
                return date(value['year'], value['month'], value['day'])
            except:
                continue
    
    tokens = alice_request.request.nlu.tokens
    
    for i in range(len(tokens)-1):
        if tokens[i].isdigit() and tokens[i+1] in month_numbers:
            day = int(tokens[i])
            month = month_numbers[tokens[i+1]]
            year = today.year
            try:
                return date(year, month, day)
            except:
                continue
    for token in tokens:
        matching_weekdays = []
        day_name = normalize_day_name(token)
        if day_name in weekday_dict.values():
            for key, value in weekday_dict.items():
                if value == day_name:
                    matching_weekdays.append(key)
            target_weekday = matching_weekdays[0]
            days_ahead = target_weekday - today.isoweekday()
            if days_ahead < 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
    
    return today