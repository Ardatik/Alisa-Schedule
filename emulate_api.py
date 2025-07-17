from fastapi import FastAPI, APIRouter, HTTPException
import json
from serialization_api import Schedule
from pydantic import ValidationError


app = FastAPI()
router = APIRouter()

@router.get('/mavrodi')
def emulate_mavrodi_schdeule():
    try:
        with open('2.json', encoding='utf-8') as f:
            data = json.load(f)
            Schedule.model_validate(data)
            return data
    except ValidationError as e:
        print('ploho')
        raise HTTPException(status_code=500, detail=f"Data validation error: {e}")
    
@router.get('/savva')
def emulate_savva_schdeule():
    try:
        with open('1.json', encoding='utf-8') as f:
            data = json.load(f)
            Schedule.model_validate(data)
            return data
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Data validation error: {e}")