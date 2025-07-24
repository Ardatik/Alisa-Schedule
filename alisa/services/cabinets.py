from schemas.alice_request import Nlu

cabinets = {
    "507А": "API_CABINET507",  
}

CABINETS_KEYWORDS = ['аудитория', 'ауд', 'кабинет']

def find_cabinet(nlu):
    tokens = [token.lower() for token in nlu.tokens]
    cabinet_numbers = list(cabinets.keys())
    for i, token in enumerate(tokens):
        if token in CABINETS_KEYWORDS and i+1 < len(tokens):
            next_token = tokens[i+1]
            if next_token in cabinet_numbers:
                return cabinets[next_token]
            for number in cabinet_numbers:
                if number.startswith(next_token) or next_token.startswith(number):
                    return cabinets[number]
    for token in tokens:
        if token in cabinet_numbers:
            return cabinets[token]
        for number in cabinet_numbers:
            if number in token or token in number:
                return cabinets[number]
    return None