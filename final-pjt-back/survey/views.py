from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SurveyForm
from .models import SurveyResponse
from .utils import calculate_score

@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
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

# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('mainpage:mainpage')

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('mainpage:mainpage')
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)