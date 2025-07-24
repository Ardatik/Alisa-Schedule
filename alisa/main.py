from fastapi import FastAPI
import uvicorn
from schemas.alice_request import AliceRequest
from services.parse_data import parse_date
from services.schedule_processing import out_readable_text
from datetime import date
from routers.emulate_api import router
from dotenv import load_dotenv
from services.teachers import init_teachers, find_teachers
from services.cabinets import find_cabinet

app = FastAPI()
app.include_router(router)
load_dotenv()
init_teachers()

@app.post('/webhook')
async def handler(request_data: AliceRequest):
    try:
        user_input = request_data.request.original_utterance.strip()
        session = request_data.session
        nlu = request_data.request.nlu
        
        response = {
            "version": request_data.version,
            "session": session,
            "response": {
                "end_session": False,
                "text": ""
            }
        }
        
        target_date = parse_date(request_data)
        
        if not user_input:
            response['response']['text'] = 'Привет, это голосовой помощник, назовите фамилию преподавателя и дату или номер аудитории'
        else:
            cabinet_api_key = find_cabinet(nlu)
            if cabinet_api_key:
                schedule_text = await out_readable_text(target_date, cabinet_api_key, entity_type="cabinet")
                response['response']['text'] = schedule_text
            else:
                found_teachers = find_teachers(nlu)
                
                if not found_teachers:
                    response['response']['text'] = (
                        'Не найдено ни преподавателя, ни аудитории. Пожалуйста, уточните запрос. '
                        'Примеры: "Расписание преподавателя Иванова на завтра" или "Аудитория 305а на среду"'
                    )
                elif len(found_teachers) == 1:
                    teacher = found_teachers[0]
                    schedule_text = await out_readable_text(target_date, teacher['api_key'])
                    response['response']['text'] = schedule_text
                else:
                    teacher_list = "\n".join([i['full_name'] for i in found_teachers])
                    response['response']['text'] = (
                        "Найдено несколько преподавателей:\n" 
                        f"{teacher_list}\n"
                        "Пожалуйста, уточните ФИО преподавателя и дату в следующем запросе, например: "
                        "\"Расписание для Иванова Ивана Ивановича на 1 сентября\""
                    )
        
        return response
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return {
            "version": request_data.version,
            "session": request_data.session,
            "response": {
                "end_session": True,
                "text": f"Произошла ошибка: {str(e)}"
            }
        }
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)