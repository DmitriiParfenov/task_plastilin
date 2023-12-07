import requests
from config.settings import API_KEY


def get_currency_rate(currency, action_currencies=None):
    """Функция возвращает актуальные курсы в отношение <currency>."""

    if action_currencies is None:
        action_currencies = ['GBP', 'USD', 'EUR', 'CNY']
        if currency not in action_currencies:
            return None
        action_currencies.remove(currency.upper())
    symbols = ','.join(action_currencies)
    url = "https://api.apilayer.com/exchangerates_data/latest"
    param = {
        "symbols": symbols,
        "base": currency,
    }
    response = requests.get(url, headers={'apikey': API_KEY}, params=param)
    if response.ok:
        return response.json().get('rates')
    else:
        return None
