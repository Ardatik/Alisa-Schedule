import pymorphy3
from typing import List

morph = pymorphy3.MorphAnalyzer()

def get_surname_forms(surname: str) -> List[str]:
    parsed = morph.parse(surname)[0]
    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
    forms = set()
    forms.add(surname.lower()) 
    for case in cases:
        try:
            form = parsed.inflect({case}).word
            forms.add(form.lower())
        except:
            continue 
    return list(forms)