from fastapi import APIRouter, HTTPException
import json
from schemas.schedule import Schedule
from pydantic import ValidationError

router = APIRouter()

@router.get('/mavrodi')
def emulate_mavrodi_schdeule():
    try:
        with open('json/2.json', encoding='utf-8') as f:
            data = json.load(f)
            Schedule.model_validate(data)
            return data
    except ValidationError as e:
        print('ploho')
        raise HTTPException(status_code=500, detail=f"Data validation error: {e}")
    
@router.get('/savva')
def emulate_savva_schdeule():
    try:
        with open('json/1.json', encoding='utf-8') as f:
            data = json.load(f)
            Schedule.model_validate(data)
            return data
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Data validation error: {e}")
    
@router.get('/cabinet507')
def emulate_cabinet507_schdeule():
    try:
        with open('json/cabinet_507.json', encoding='utf-8') as f:
            data = json.load(f)
            Schedule.model_validate(data)
            return data
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Data validation error: {e}")
    
@router.get('/mavrodi_tomorrow')
def emulate_mavrodi_tomorrow_schedule():
    try:
        with open('json/tomorrow.json', encoding='utf-8') as f:
            data = json.load(f)
            Schedule.model_validate(data)
            return data
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=f"Data validation error: {e}")