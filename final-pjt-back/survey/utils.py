def calculate_score(survey_response):
    # 점수 매기기
    age_group_scores = {'10대': 2, '20대': 4, '30~40대': 3, '50대': 2, '60세 이상': 1}
    asset_ratio_scores = {'5% 이하': 5, '10% 이하': 4, '20% 이하': 3, '30% 이하': 2, '30% 초과': 1}
    expected_return_scores = {'원금 보존이 무조건!': 1, '예적금 수익률보다 3% 이상 기대 가능하다면 원금보존 가능성이 조금 낮아져도': 3, 'High Risk - High Return': 5}
    financial_knowledge_scores = {'투자의사 결정 스스로 내려본 경험 없음': 1, '주식과 채권, 예금과 적금을 구분할 수 있음': 2, '투자할 수 있는 대부분의 금융상품 차이를 구별할 수 있음': 3, '금융상품과 투자대상 상품의 차이 이해할 수 있음': 4, 'Master': 5}

    # 설문조사 결과에서 선택된 항목에 대한 점수 가져오기
    age_group_score = age_group_scores.get(survey_response.age_group, 0)
    asset_ratio_score = asset_ratio_scores.get(survey_response.asset_ratio, 0)
    expected_return_score = expected_return_scores.get(survey_response.expected_return, 0)
    financial_knowledge_score = financial_knowledge_scores.get(survey_response.financial_knowledge, 0)

    # 총점 계산
    total_score = age_group_score + asset_ratio_score + expected_return_score + financial_knowledge_score

    return total_score

# 설문조사 결과 저장 후 점수 계산 및 저장
def save_survey_response_with_score(form, user):
    survey_response = form.save(commit=False)
    survey_response.user = user
    survey_response.save()

    # 점수 계산
    total_score = calculate_score(survey_response)

    # 사용자 프로필에 점수 저장
    user.profile.score = total_score
    user.profile.save()
