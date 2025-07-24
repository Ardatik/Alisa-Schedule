from typing import Dict, List
from schemas.alice_request import Nlu, Entity
from .morph import get_surname_forms

teachers_info = {}
surname_forms = {}
full_name_index = {}

def add_teacher(surname, full_name, api_key):
    teachers_info[api_key] = {
        'full_name': full_name,
        'surname': surname,
        'api_key': api_key
    }
    forms = get_surname_forms(surname)
    for form in forms:
        if form not in surname_forms:
            surname_forms[form] = []
        if api_key not in surname_forms[form]:
            surname_forms[form].append(api_key)
    name_parts = full_name.lower().split()
    for part in name_parts:
        if part not in full_name_index:
            full_name_index[part] = []
        if api_key not in full_name_index[part]:
            full_name_index[part].append(api_key)

def init_teachers():
    teachers_list = [
        ("Абакумова", "Абакумова Виктория Вячеславовна", "API_ABAKUMOBA"),
        ("Мавроди", "Мавроди Николай Николаевич", "API_MAVRODI2"),
        ("Мавроди", "Мавроди Сергей Пантелеевич", "API_MAVRODI"),
        ("Савва", "Савва Елена Владимировна", "API_SAVVA"),
    ]
    for surname, full_name, api_key in teachers_list:
        add_teacher(surname, full_name, api_key)

def find_teachers(nlu: Nlu) -> List[dict]:
    fio_data = {}
    for entity in nlu.entities:
        if entity.type == 'YANDEX.FIO':
            fio_data = entity.value
            break

    if fio_data and fio_data.get('last_name', '').lower() in ['на', 'для']:
        fio_data['last_name'] = ''

    last_name = fio_data.get('last_name', '').lower()
    first_name = fio_data.get('first_name', '').lower()
    patronymic = fio_data.get('patronymic_name', '').lower()

    if last_name and first_name and patronymic:
        full_name = f"{last_name} {first_name} {patronymic}"
        for teacher in teachers_info.values():
            if teacher['full_name'].lower() == full_name:
                return [teacher]
        return []

    if (first_name or patronymic) and not last_name:
        name_parts = []
        if first_name:
            name_parts.append(first_name)
        if patronymic:
            name_parts.append(patronymic)
        
        candidates = []
        for teacher in teachers_info.values():
            teacher_name = teacher['full_name'].lower()
            if all(part in teacher_name.split() for part in name_parts):
                candidates.append(teacher)
        return candidates

    if last_name and not (first_name or patronymic):
        if last_name in surname_forms:
            api_keys = surname_forms[last_name]
            return [teachers_info[key] for key in api_keys]
    
    return []