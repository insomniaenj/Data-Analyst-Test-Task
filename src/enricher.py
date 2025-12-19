import requests
from bs4 import BeautifulSoup
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def analyze_company(company_data):
    session = requests.Session()
    session.proxies = {'http': None, 'https': None}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    res = {
        'site': 'N/A', 'support_team_size_min': 0, 'support_evidence': '',
        'evidence_url': company_data['sample_vacancy_url'], 'evidence_type': 'jobs',
        'has_support_email': 0, 'has_online_chat': 0, 'has_kb_or_faq': 0,
        'mentions_24_7': 0, 'inn': 'Unknown'
    }

    try:
        emp_id = company_data['hh_id']
        emp_resp = session.get(f"https://api.hh.ru/employers/{emp_id}", headers=headers, timeout=5)
        if emp_resp.status_code == 200:
            emp_info = emp_resp.json()
            res['site'] = emp_info.get('site_url', 'N/A')
            search_area = str(emp_info) + (emp_info.get('description') or "")
            inn_found = re.search(r'\b(\d{10}|\d{12})\b', search_area)
            if inn_found:
                res['inn'] = inn_found.group(1)

        vac_id = company_data['sample_vacancy_url'].split('/')[-1].split('?')[0]
        vac_resp = session.get(f"https://api.hh.ru/vacancies/{vac_id}", headers=headers, timeout=5)

        if vac_resp.status_code == 200:
            vac_info = vac_resp.json()
            desc = vac_info.get('description', '')

            if res['inn'] == 'Unknown':
                inn_vac = re.search(r'ИНН\s*:?\s*(\d{10}|\d{12})', desc)
                if inn_vac: res['inn'] = inn_vac.group(1)

            size_match = re.search(r'(?:команда|штат|отдел|поддержк\w+)\s+(?:из|более|около)?\s*(\d{2,3})', desc, re.I)
            if size_match:
                val = int(size_match.group(1))
                if val >= 10:
                    res['support_team_size_min'] = val
                    res['support_evidence'] = f"Упоминание размера команды ({val} чел.)"

            if res['support_team_size_min'] < 10:
                low_desc = desc.lower()
                if any(x in low_desc for x in ['24/7', 'круглосуточн', 'сменн', 'ночные смены', 'график 2/2']):
                    res['support_team_size_min'] = 12
                    res['support_evidence'] = "Оценка 10+ на основании сменного графика работы (24/7)"
                    res['mentions_24_7'] = 1

        if res['site'] != 'N/A' and res['site'].startswith('http'):
            try:
                s_resp = session.get(res['site'], timeout=7, headers=headers, verify=False)
                html = s_resp.text.lower()

                if any(x in html for x in ['support@', 'help@', 'service@', 'info@']): res['has_support_email'] = 1
                if any(x in html for x in ['faq', 'база знаний', 'вопросы и ответы']): res['has_kb_or_faq'] = 1
                if any(x in html for x in ['jivo', 'bitrix', 'widget', 'chat', 'webim']): res['has_online_chat'] = 1
                if '24/7' in html or 'круглосуточно' in html: res['mentions_24_7'] = 1

                if res['inn'] == 'Unknown':
                    inn_site = re.search(r'\b(\d{10}|\d{12})\b', html)
                    if inn_site: res['inn'] = inn_site.group(1)
            except:
                pass
    except:
        pass

    return res