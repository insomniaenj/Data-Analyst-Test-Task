import requests
import time
from tqdm import tqdm


def get_companies_with_support():
    print(">>> Шаг 1: Сбор компаний (расширенный поиск)...")
    url = "https://api.hh.ru/vacancies"
    companies = {}

    queries = ['поддержка', 'helpdesk', 'контакт-центр', 'клиентский сервис', 'call-центр']

    for q in queries:
        for page in range(3):
            params = {
                'text': q,
                'area': 113,
                'per_page': 100,
                'page': page
            }
            try:
                resp = requests.get(url, params=params, timeout=5).json()
                items = resp.get('items', [])
                for item in items:
                    emp = item.get('employer')
                    if emp and emp.get('id'):
                        eid = emp['id']
                        if eid not in companies:
                            companies[eid] = {
                                'hh_id': eid,
                                'name': emp['name'],
                                'sample_vacancy_url': item.get('alternate_url')
                            }
                time.sleep(0.1)
            except:
                continue

    return list(companies.values())