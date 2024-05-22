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
# import pandas as pd

# API_key = settings.FIN_API_KEY
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# Create your views here.

bank_deposit = []
bank_saving = []
@api_view(['GET'])
def index(request): # DB에 저장기능 통합
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
    
    for data in baseList_deposit: ## 은행 종류 select바에 넣기
        if data['kor_co_nm'] not in bank_deposit:
            bank_deposit.append(data['kor_co_nm'])
    for data in baseList_saving: ## 은행 종류 select바에 넣기
        if data['kor_co_nm'] not in bank_saving:
            bank_saving.append(data['kor_co_nm'])
    context = {
        'bank_deposit': bank_deposit,
        'bank_saving': bank_saving
    }

    return render(request, 'finlife/index.html', context)


@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        depositProducts = DepositProducts.objects.all()
        serializers = DepositProductsSerializer(depositProducts, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        # sample = {
        #     'fin_prdt_cd': 'TEST001',
        #     'kor_co_nm': 'SSAFY은행',
        #     'fin_prdt_nm': '구레잇9기예금',
        #     'etc_note': '자유',
        #     'join_deny': 1,
        #     'join_member': '실명의 개인',
        #     'join_way': '스마트폰',
        #     'spcl_cnd': '해당사항 없음'
        # }
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializers.data)



@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):

    depositOptions = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializers = DepositOptionsSerializer(depositOptions, many=True)
    return Response(serializers.data)



@api_view(['GET'])
def top_rate(request):
    depositOptions = DepositOptions.objects.order_by('intr_rate2').first()
    serializers_option = DepositOptionsSerializer(depositOptions)

    product = DepositProducts.objects.get(pk=depositOptions.product.pk)
    # print(product)
    serializers_product = DepositProductsSerializer(product)
    return Response({'deposit_products':serializers_product.data, 'options':[serializers_option.data]})

@api_view(['GET'])
def sort_rate(request):
    # intr_rate2 필드를 기준으로 DepositOptions를 정렬
    deposit_options = DepositOptions.objects.all().order_by('intr_rate2')
    serializers_option = DepositOptionsSerializer(deposit_options, many=True)

    # 정렬된 DepositOptions 중 각각에 해당하는 DepositProducts를 가져와서 직렬화
    products = [option.product for option in deposit_options]
    serializers_product = DepositProductsSerializer(products, many=True)


    # DepositProducts와 DepositOptions를 번갈아가며 출력
    output_data = []
    for product, option in zip(serializers_product.data, serializers_option.data):
        output_data.append(product)
        output_data.append(option)

    return Response({'data': output_data})


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
