from serialization_api import Schedule
from dotenv import load_dotenv
import os
import httpx
from datetime import date

def process_data_to_text(data, target_date):
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
    
async def out_readable_text(date, api_from_env):
    api_url = os.getenv(api_from_env)
    print(api_url)
    if not api_url:
        print(f"Ошибка: Не найдена переменная окружения {api_from_env}")
        return "Ошибка"
    async with httpx.AsyncClient() as client:
        try:  
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
            return process_data_to_text(data, date)
        except httpx.HTTPStatusError as exc:
            print(f"Ошибка при получении расписания: {exc.response.status_code}")
            return "Ошибка при получении расписания"
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            return "Произошла ошибка"
        
        
        
        
import asyncio
load_dotenv()
result = asyncio.run(out_readable_text(date(2025, 9, 1), "API_ABAKUMOBA"))
print(result)
            
        