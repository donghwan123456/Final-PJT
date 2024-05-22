from django.shortcuts import render
from .services import get_exchange_rates, get_historical_rates
from datetime import datetime, timedelta
def home(request):
    exchange_rates = get_exchange_rates()
    today = datetime.now()

    return render(request, 'exchange_app/home.html', {'exchange_rates': exchange_rates, 'today': today})


def calculator(request):
    exchange_rates = get_exchange_rates()
    historical_rates = {'dates': [], 'rates': []}

    if request.method == 'POST':
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')
        amount = float(request.POST.get('amount'))

        from_rate = next(rate for rate in exchange_rates if rate['cur_unit'] == from_currency)
        to_rate = next(rate for rate in exchange_rates if rate['cur_unit'] == to_currency)

        from_rate_value = float(from_rate['bkpr'].replace(',', ''))
        to_rate_value = float(to_rate['bkpr'].replace(',', ''))

        # KRW는 1000원 단위로 계산
        if from_currency == 'KRW':
            converted_amount = (amount / 1000) * to_rate_value
        elif to_currency == 'KRW':
            converted_amount = (amount / from_rate_value) * (1000 / to_rate_value)
        else:
            converted_amount = (amount / from_rate_value) * to_rate_value

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        historical_rates = get_historical_rates(from_currency, start_date, end_date)

        context = {
            'exchange_rates': exchange_rates,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'converted_amount': f"{converted_amount:,.2f}",
            'historical_rates': historical_rates,
        }
        return render(request, 'exchange_app/calculator.html', context)

    return render(request, 'exchange_app/calculator.html', {'exchange_rates': exchange_rates})