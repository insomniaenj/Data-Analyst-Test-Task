import re

def clean_text(text):
    if not text: return ""
    return re.sub(r'\s+', ' ', text).strip()

def extract_inn(text):
    match = re.search(r'\b\d{10}(\d{2})?\b', text)
    return match.group(0) if match else None

def find_support_number(text):
    patterns = [
        r'(?:команда|штат|отдел|поддержк\w+)\s+(?:состоит\s+из\s+)?(?:более|около|до)?\s*(\d{2,3})\s+(?:человек|сотрудник|оператор)',
        r'(\d{2,3})\s+(?:человек|сотрудник|оператор)\s+в\s+(?:команде|поддержке|саппорте)'
    ]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None