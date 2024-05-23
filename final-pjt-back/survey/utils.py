def calculate_score(survey_response):
    # 점수 매기기
    age_scores = [(0, 19, 2), (20, 29, 4), (30, 49, 3), (50, 59, 2), (60, 120, 1)]
    asset_ratio_scores = {'5% 이하': 5, '10% 이하': 4, '20% 이하': 3, '30% 이하': 2, '30% 초과': 1}
    expected_return_scores = {'원금 보존이 무조건!': 1, '예적금 수익률보다 3% 이상 기대 가능하다면 원금보존 가능성이 조금 낮아져도': 3, 'High Risk - High Return': 5}
    financial_knowledge_scores = {'투자의사 결정 스스로 내려본 경험 없음': 1, '주식과 채권, 예금과 적금을 구분할 수 있음': 2, '투자할 수 있는 대부분의 금융상품 차이를 구별할 수 있음': 3, '금융상품과 투자대상 상품의 차이 이해할 수 있음': 4, 'Master': 5}

    # 나이 점수 계산
    age_score = 0
    for min_age, max_age, score in age_scores:
        if min_age <= survey_response.age <= max_age:
            age_score = score
            break
    
    asset_ratio_score = asset_ratio_scores.get(survey_response.asset_ratio, 0)
    expected_return_score = expected_return_scores.get(survey_response.expected_return, 0)
    financial_knowledge_score = financial_knowledge_scores.get(survey_response.financial_knowledge, 0)

    # 총점 계산
    total_score = age_score + asset_ratio_score + expected_return_score + financial_knowledge_score

    return total_score

# 설문조사 결과 저장 후 점수 계산 및 저장
def save_survey_response_with_score(form, user):
    survey_response = form.save(commit=False)
    survey_response.user = user
    survey_response.save()

    # 점수 계산
    total_score = calculate_score(survey_response)

    # 설문조사 응답에 점수 저장
    survey_response.score = total_score
    survey_response.save()


# utils.py

import re

# utils.py

import re

def is_eligible(join_member, user_age):
    # 숫자와 '이상', '이하' 키워드 추출
    age_ranges = re.findall(r'(\d+)(이상|이하|)', join_member)
    
    # 단순히 '개인'인 경우는 모든 연령대가 해당되므로 True 반환
    if '개인' in join_member and not age_ranges:
        return True
    
    for age, condition in age_ranges:
        age = int(age)
        if condition == '이상' and user_age >= age:
            return True
        elif condition == '이하' and user_age <= age:
            return True

    # 나이 범위가 명시된 경우 처리
    range_match = re.search(r'(\d+)\s*~\s*(\d+)', join_member)
    if range_match:
        min_age, max_age = map(int, range_match.groups())
        if min_age <= user_age <= max_age:
            return True

    return False
