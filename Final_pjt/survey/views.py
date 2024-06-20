from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SurveyForm
from .models import SurveyResponse
from .utils import calculate_score, is_eligible
from finlife.models import DepositProducts, SavingProducts
from finlife.models import DepositOptions, SavingOptions

@login_required
def index(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # 사용자가 이전에 제출한 설문 결과가 있는지 확인
            existing_survey_response = SurveyResponse.objects.filter(user=request.user).first()
            if existing_survey_response:
                # 이미 설문 결과가 있는 경우 삭제
                existing_survey_response.delete()

            # 설문 결과 저장
            survey_response = form.save(commit=False)
            survey_response.user = request.user
            survey_response.save()

            total_score = calculate_score(survey_response)
            survey_response.score = total_score
            survey_response.save()

            return redirect('mainpage:mainpage')  # 설문 제출 완료 후 이동할 페이지
    else:
        form = SurveyForm()
    context = {
        'form': form,
    }
    
    return render(request, 'survey/index.html', context)


@login_required
def recommend_products(request):
    # 사용자 설문조사 결과 가져오기
    survey_response = SurveyResponse.objects.filter(user=request.user).first()
    if not survey_response:
        return redirect('survey:index')
    
    # 설문조사 점수 계산
    score = calculate_score(survey_response)
    
    # 적금 및 예금 상품 전체 가져오기
    saving_products = SavingProducts.objects.prefetch_related('options').all()
    deposit_products = DepositProducts.objects.prefetch_related('options').all()
    
    # 나이 제한에 맞는 상품 필터링
    saving_products = [
        product for product in saving_products if is_eligible(product.join_member, survey_response.age)
    ]
    deposit_products = [
        product for product in deposit_products if is_eligible(product.join_member, survey_response.age)
    ]
    
    def get_middle_products(products, key):
        sorted_products = sorted(products, key=key)
        middle_index = len(sorted_products) // 2
        # 중간값 근처 3개 상품 선택 (중간값을 포함하여 앞뒤로 하나씩)
        return sorted_products[max(0, middle_index-1):middle_index+2]

    # 점수에 따른 상품 추천
    if score <= 7:
        # 안정적인 예적금 상품 추천
        deposit_products = sorted(deposit_products, key=lambda x: x.options.first().intr_rate)[:3]
        saving_products = sorted(saving_products, key=lambda x: x.options.first().intr_rate)[:3]
    elif 7 < score <= 12:
        # 중간 리스크 예적금 상품 추천
        deposit_products = get_middle_products(deposit_products, key=lambda x: x.options.first().intr_rate)
        saving_products = get_middle_products(saving_products, key=lambda x: x.options.first().intr_rate)
    else:
        # 고수익 예적금 상품 추천
        deposit_products = sorted(deposit_products, key=lambda x: x.options.first().intr_rate2, reverse=True)[:3]
        saving_products = sorted(saving_products, key=lambda x: x.options.first().intr_rate2, reverse=True)[:3]
    
    additional_recommendations = None
    if score > 15:
        additional_recommendations = [
            {'name': '금융 투자 협회', 'url': 'https://freesis.kofia.or.kr/'},
            {'name': '업비트', 'url': 'https://upbit.com/home'},
            {'name': '네이버 증권', 'url': 'https://m.stock.naver.com/'},
        ]
    
    context = {
        'deposit_products': deposit_products,
        'saving_products': saving_products,
        'additional_recommendations': additional_recommendations,
    }
    
    return render(request, 'survey/recommendations.html', context)
