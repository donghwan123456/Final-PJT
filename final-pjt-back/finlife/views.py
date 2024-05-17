import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
from .models import DepositProducts, DepositOptions

# API_key = settings.FIN_API_KEY
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# Create your views here.

@api_view(['GET'])
def index(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo': 1
    }
    
    response = requests.get(URL, params=params).json()
    return JsonResponse({ 'response': response })


@api_view(['GET'])
def save_deposit_products(request):
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo' : '020000',
        'pageNo': 1
    }
    response = requests.get(URL, params=params).json()

    result = response.get('result')
    baseList = result['baseList']
    optionList = result['optionList']
    

    for li in baseList:
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')

        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm': fin_prdt_nm,
            'etc_note': etc_note,
            'join_deny': join_deny,
            'join_member': join_member,
            'join_way': join_way,
            'spcl_cnd': spcl_cnd,
        }

        for k,v in save_data.items():
            if not v: # 값이 비어있으면 -1 할당
                save_data[k] = -1 

        serializer = DepositProductsSerializer(data=save_data)
        # 유효성 검증
        if serializer.is_valid(raise_exception=True):
            # 유효하다면, 저장
            serializer.save()
    
    for li in optionList:
        product = li.get('product')
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        intr_rate = li.get('intr_rate')
        intr_rate2 = li.get('intr_rate2')
        save_trm = li.get('save_trm')

        save_data = {
            'product': product,
            'fin_prdt_cd': fin_prdt_cd,
            'intr_rate_type_nm': intr_rate_type_nm,
            'intr_rate': intr_rate,
            'intr_rate2': intr_rate2,
            'save_trm': save_trm,
        }
        for k,v in save_data.items():
            if not v: # 값이 비어있으면 -1 할당
                save_data[k] = -1 

        serializer = DepositOptionsSerializer(data=save_data)
        # 유효성 검증
        if serializer.is_valid(raise_exception=True):
            # 유효하다면, 저장
            
            serializer.save(product = DepositProducts.objects.get(fin_prdt_cd=li['fin_prdt_cd']))

    return JsonResponse({ "message": "save okay!" })


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
def filter(request, kor_co_nm):
    depositProducts = DepositProducts.objects.filter(kor_co_nm=kor_co_nm)
    serializers = DepositProductsSerializer(depositProducts, many=True)
    return Response(serializers.data)