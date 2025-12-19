from bs4 import BeautifulSoup
import requests


def scrape_site_features(url):
    features = {
        'has_support_email': False,
        'has_online_chat': False,
        'mentions_24_7': False,
        'chat_vendor': None
    }
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'lxml')
        text = soup.get_text().lower()

        if '24/7' in text or 'круглосуточно' in text:
            features['mentions_24_7'] = True

        if 'support@' in text or 'help@' in text:
            features['has_support_email'] = True

        html = r.text.lower()
        if 'jivo' in html:
            features['chat_vendor'] = 'Jivo'
        elif 'intercom' in html:
            features['chat_vendor'] = 'Intercom'

    except:
        pass
    return features