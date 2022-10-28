import requests
from decouple import config

headers = {
    'Content-Type': 'application/json',
    'Authorization': config("TOKEN")
}


def get_meta_data(ticker):
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}'
    response = requests.get(url, headers=headers)
    return response.json()


def get_price_data(ticker):
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices'
    response = requests.get(url, headers=headers)
    return response.json()[0]
