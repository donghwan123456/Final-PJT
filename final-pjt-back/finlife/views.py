import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from .models import DepositProducts, DepositOptions
from .serializers import SavingProductsSerializer, SavingOptionsSerializer
from .models import SavingProducts, SavingOptions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# import pandas as pd

# API_key = settings.FIN_API_KEY
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# Create your views here.

@login_required
def index(request):
    URL_deposit = BASE_URL + 'depositProductsSearch.json'
    URL_saving = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo': 1
    }
    response_deposit = requests.get(URL_deposit, params=params).json()
    response_saving = requests.get(URL_saving, params=params).json()

    result_deposit = response_deposit.get('result')
    baseList_deposit = result_deposit['baseList']
    optionList_deposit = result_deposit['optionList']

    result_saving = response_saving.get('result')
    baseList_saving = result_saving['baseList']
    optionList_saving = result_saving['optionList']

    def fill_missing(data, default_value=-1):
        return {k: (v if v is not None else default_value) for k, v in data.items()}

    # baseList 예금 처리
    for base_data in baseList_deposit:
        base_data = fill_missing(base_data)  # 결측값 처리
        fin_prdt_cd = base_data['fin_prdt_cd']

        # 중복 체크: 이미 데이터베이스에 있는지 확인
        if not DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            serializer = DepositProductsSerializer(data=base_data)
            if serializer.is_valid(raise_exception=True):
                product = serializer.save()
            # print('save!')


    # optionList 예금 처리
    for option_data in optionList_deposit:
        option_data = fill_missing(option_data)  # 결측값 처리
        fin_prdt_cd = option_data['fin_prdt_cd']

        # 중복 체크: 이미 데이터베이스에 있는지 확인
        if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            
            # 옵션이 이미 존재하는지 확인
            if not DepositOptions.objects.filter(
                product=product,
                intr_rate_type_nm=option_data['intr_rate_type_nm'],
                intr_rate=option_data['intr_rate'],
                intr_rate2=option_data['intr_rate2'],
                save_trm=option_data['save_trm']
            ).exists():
                option_serializer = DepositOptionsSerializer(data=option_data)
                if option_serializer.is_valid(raise_exception=True):
                    option_serializer.save(product=product)
                # print('save!!')

    # baseList 적금 처리
    for base_data in baseList_saving:
        base_data = fill_missing(base_data)  # 결측값 처리
        fin_prdt_cd = base_data['fin_prdt_cd']

        # 중복 체크: 이미 데이터베이스에 있는지 확인
        if not SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            serializer = SavingProductsSerializer(data=base_data)
            if serializer.is_valid(raise_exception=True):
                product = serializer.save()
            # print('save!!#')


    # optionList 적금 처리
    for option_data in optionList_saving:
        option_data = fill_missing(option_data)  # 결측값 처리
        fin_prdt_cd = option_data['fin_prdt_cd']

        # 중복 체크: 이미 데이터베이스에 있는지 확인
        if SavingProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            
            # 옵션이 이미 존재하는지 확인
            if not SavingOptions.objects.filter(
                product=product,
                intr_rate_type_nm=option_data['intr_rate_type_nm'],
                intr_rate=option_data['intr_rate'],
                intr_rate2=option_data['intr_rate2'],
                save_trm=option_data['save_trm'],
                rsrv_type=option_data['rsrv_type'],
                rsrv_type_nm=option_data['rsrv_type_nm'],
            ).exists():
                option_serializer = SavingOptionsSerializer(data=option_data)
                if option_serializer.is_valid(raise_exception=True):
                    option_serializer.save(product=product)
                # print('save!!##')

    bank_deposit = DepositProducts.objects.values_list('kor_co_nm', flat=True).distinct()
    bank_saving = SavingProducts.objects.values_list('kor_co_nm', flat=True).distinct()

    deposit_products = DepositProducts.objects.all()
    saving_products = SavingProducts.objects.all()

    selected_bank = request.GET.get('bank')
    if selected_bank:
        deposit_products = deposit_products.filter(kor_co_nm=selected_bank)
        saving_products = saving_products.filter(kor_co_nm=selected_bank)

    context = {
        'bank_deposit': bank_deposit,
        'bank_saving': bank_saving,
        'deposit_products': deposit_products,
        'saving_products': saving_products,
        'selected_bank': selected_bank,
    }
    return render(request, 'finlife/index.html', context)



@api_view(['GET'])
def filter(request):
    kor_co_nm = request.GET.get('bank')
    product_type = request.GET.get('product_type')

    if product_type == 'deposit':
        # DepositProducts 필터링
        products = DepositProducts.objects.filter(kor_co_nm=kor_co_nm)
        serializers_product = DepositProductsSerializer(products, many=True)

        # DepositProducts에 연결된 DepositOptions 필터링
        options = DepositOptions.objects.filter(product__in=products)
        serializers_option = DepositOptionsSerializer(options, many=True)
        # serializers_option = serializers_option.get('kor_co_nm')

    elif product_type == 'saving':
        products = SavingProducts.objects.filter(kor_co_nm=kor_co_nm)
        serializers_product = SavingProductsSerializer(products, many=True)

        # DepositProducts에 연결된 DepositOptions 필터링
        options = SavingOptions.objects.filter(product__in=products)
        serializers_option = SavingOptionsSerializer(options, many=True)

    # DepositProducts와 DepositOptions를 번갈아가며 출력
    product_data = []
    option_data = []
    for product in serializers_product.data:
        product_data.append(product)
        product_options = [option for option in serializers_option.data if option['product'] == product['id'] and 6 <= option['save_trm'] <= 36]
        sorted_product_options = sorted(product_options, key=lambda x: x['save_trm'])  # save_trm 기준으로 오름차순 정렬
        option_data.extend(sorted_product_options)

    context = {
        'deposit_products': product_data,
        'deposit_options' : option_data,
        # 'deposit_products': serializers_product.data,
        'selected_bank': kor_co_nm
    }
    # print(option_data[0])
    return render(request, 'finlife/filter.html', context)

def compare_products(request):
    deposit_product_ids = request.GET.getlist('deposit_products')
    saving_product_ids = request.GET.getlist('saving_products')
    
    deposit_products = DepositProducts.objects.filter(id__in=deposit_product_ids)
    saving_products = SavingProducts.objects.filter(id__in=saving_product_ids)

    context = {
        'deposit_products': deposit_products,
        'saving_products': saving_products,
    }

    return render(request, 'finlife/compare.html', context)

@login_required
def product_detail(request, product_type, product_id):
    if product_type == 'deposit':
        product = get_object_or_404(DepositProducts, id=product_id)
        enrolled = product in request.user.enrolled_deposit_products.all()
    else:
        product = get_object_or_404(SavingProducts, id=product_id)
        enrolled = product in request.user.enrolled_saving_products.all()

    context = {
        'product': product,
        'product_type': product_type,
        'enrolled': enrolled,
    }
    return render(request, 'finlife/detail.html', context)

@login_required
def enroll_product(request, product_type, product_id):
    if product_type == 'deposit':
        product = get_object_or_404(DepositProducts, id=product_id)
        if product in request.user.enrolled_deposit_products.all():
            request.user.enrolled_deposit_products.remove(product)
        else:
            request.user.enrolled_deposit_products.add(product)
    else:
        product = get_object_or_404(SavingProducts, id=product_id)
        if product in request.user.enrolled_saving_products.all():
            request.user.enrolled_saving_products.remove(product)
        else:
            request.user.enrolled_saving_products.add(product)
    request.user.save()

    return redirect('accounts:profile', username=request.user.username)