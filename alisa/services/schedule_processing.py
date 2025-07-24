from schemas.schedule import Schedule
import os
import httpx

def process_data_to_text_for_teachers(data, target_date):
    schedule_list = []
    schedule = Schedule.model_validate(data)
    for i in schedule.data:
        if i.date == target_date:
            if i.place:
                i.place = i.place.name
            else:
                i.place = 'не указана'
            text = (
                f"Пара номер {i.number}, "
                f"тип: {i.type.name}, "
                f"дисциплина: {i.discipline.name}, "
                f"группы: {', '.join([group.name for group in i.groups])}, "
                f"аудитория {i.place}, "
                f"время: {i.start_time}-{i.end_time}"
            )
            schedule_list.append(text)
    if len(schedule_list) > 0:
        return ' '.join(schedule_list)
    else:
        return "На эту дату занятий не найдено"
    
def process_data_to_text_for_cabinets(data, target_date):
    schedule_list = []
    schedule = Schedule.model_validate(data)
    for i in schedule.data:
        if i.date == target_date:
            if i.place:
                i.place = i.place.name
            else:
                i.place = 'не указана'
            text = (
                f"Пара номер {i.number}, "
                f"тип: {i.type.name}, "
                f"дисциплина: {i.discipline.name}, "
                f"преподаватель: {', '.join([teacher.full_name for teacher in i.teachers])}, "
                f"аудитория {i.place}, "
                f"время: {i.start_time}-{i.end_time}"
            )
            schedule_list.append(text)
    if len(schedule_list) > 0:
        return ' '.join(schedule_list)
    else:
        return "На эту дату занятий не найдено"
    
async def out_readable_text(target_date, api_key, entity_type="teacher"):
    api_url = os.getenv(api_key)
    if not api_url:
        return f"Ошибка: не настроен API для {api_key}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
            if entity_type == "cabinet":
                return process_data_to_text_for_cabinets(data, target_date)
            else:
                return process_data_to_text_for_teachers(data, target_date)       
        except httpx.HTTPStatusError as exc:
            return f"Ошибка при получении расписания: {exc.response.status_code}"
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"