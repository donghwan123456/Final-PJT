import requests
from datetime import datetime

def get_exchange_rates():
    api_key = 'crj6Gewzk6uUjyA0rItIBsYWCEae1wRi'
    url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate=20240522&data=AP01"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return []

def get_historical_rates(currency_code, start_date, end_date):
    url = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base=USD&symbols={currency_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # 응답 데이터 구조 확인
        print(data)

        if 'rates' in data:
            historical_data = {
                'dates': list(data['rates'].keys()),
                'rates': [data['rates'][date][currency_code] for date in data['rates']]
            }
        else:
            historical_data = {'dates': [], 'rates': []}
        
        return historical_data
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return {'dates': [], 'rates': []}
