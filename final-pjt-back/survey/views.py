from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SurveyForm
from .models import SurveyResponse
from .utils import calculate_score
from finlife.models import DepositProducts, SavingProducts

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
    
    # 점수에 따른 상품 추천
    deposit_products = DepositProducts.objects.prefetch_related('options').all()
    saving_products = SavingProducts.objects.prefetch_related('options').all()
    
    if score <= 5:
        # 안정적인 예적금 상품 추천
        deposit_products = deposit_products.filter(max_limit__gte=0).order_by('options__intr_rate')[:3]
        saving_products = saving_products.filter(max_limit__gte=0).order_by('options__intr_rate')[:3]
    elif 5 < score <= 10:
        # 중간 리스크 예적금 상품 추천
        deposit_products = deposit_products.filter(max_limit__gte=0).order_by('-options__intr_rate')[:3]
        saving_products = saving_products.filter(max_limit__gte=0).order_by('-options__intr_rate')[:3]
    else:
        # 고수익 예적금 상품 추천
        deposit_products = deposit_products.filter(max_limit__gte=0).order_by('-options__intr_rate2')[:3]
        saving_products = saving_products.filter(max_limit__gte=0).order_by('-options__intr_rate2')[:3]
    
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