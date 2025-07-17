from fastapi import FastAPI
import uvicorn
from serialization_data_Alice import AliceRequest
from days import parse_date
from api_data import out_readable_text
from datetime import date
from emulate_api import router
from dotenv import load_dotenv

app = FastAPI()
app.include_router(router)
load_dotenv()

@app.post('/webhook')
async def handler(request_data: AliceRequest):
    try:
        user_input = request_data.request.original_utterance.lower().strip()
        session = request_data.session
        
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
            response['response']['text'] = 'Привет, это голосовой помощник, назовите фамилию преподавателя'
        elif 'Абакумова'.lower() in user_input:
            schedule_text = await out_readable_text(target_date, "API_ABAKUMOBA")
            response['response']['text'] = schedule_text
        elif 'Мавроди'.lower() in user_input:
            schedule_text = await out_readable_text(target_date, "API_MAVRODI")
            response['response']['text'] = schedule_text
        elif 'Савва'.lower() in user_input:
            schedule_text = await out_readable_text(target_date, "API_SAVVA")
            response['response']['text'] = schedule_text
        else:
            response['response']['text'] = 'Не смогла распознать преподавателя или день недели ли дату.'
            
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
    
