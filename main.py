import pandas as pd
from src.collect_seeds import get_companies_with_support
from src.enricher import analyze_company
from tqdm import tqdm
import os


def main():
    seeds = get_companies_with_support()

    final_data = []
    print(f">>> Шаг 2: Анализ {len(seeds)} компаний...")

    for seed in tqdm(seeds):
        info = analyze_company(seed)

        if info['support_team_size_min'] >= 10:
            row = {
                'inn': info['inn'],
                'name': seed['name'],
                'site': info['site'],
                'support_team_size_min': info['support_team_size_min'],
                'support_evidence': info['support_evidence'],
                'evidence_url': info['evidence_url'],
                'evidence_type': info['evidence_type'],
                'source': 'hh_api',
                'has_support_email': info['has_support_email'],
                'has_contact_form': 1 if info['has_online_chat'] else 0,
                'has_online_chat': info['has_online_chat'],
                'has_messengers': 1 if 't.me' in str(info) else 0,
                'has_support_section': info['has_kb_or_faq'],
                'has_kb_or_faq': info['has_kb_or_faq'],
                'mentions_24_7': info['mentions_24_7']
            }
            final_data.append(row)

        if len(final_data) >= 100:
            break

    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(final_data)
    df.to_csv('data/companies.csv', index=False, encoding='utf-8-sig')
    print(f">>> Готово! Сохранено {len(df)} компаний в data/companies.csv")


if __name__ == "__main__":
    main()