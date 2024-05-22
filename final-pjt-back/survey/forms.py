from django import forms
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    AGE_GROUP_CHOICES = [
        ('10대', '10대'),
        ('20대', '20대'),
        ('30~40대', '30~40대'),
        ('50대', '50대'),
        ('60세 이상', '60세 이상'),
    ]
    
    ASSET_RATIO_CHOICES = [
        ('5% 이하', '5% 이하'),
        ('10% 이하', '10% 이하'),
        ('20% 이하', '20% 이하'),
        ('30% 이하', '30% 이하'),
        ('30% 초과', '30% 초과'),
    ]

    EXPECTED_RETURN_CHOICES = [
        ('원금 보존이 무조건!', '원금 보존이 무조건!'),
        ('예적금 수익률보다 3% 이상 기대 가능하다면 원금보존 가능성이 조금 낮아져도', '예적금 수익률보다 3% 이상 기대 가능하다면 원금보존 가능성이 조금 낮아져도'),
        ('High Risk - High Return', 'High Risk - High Return'),
    ]

    FINANCIAL_KNOWLEDGE_CHOICES = [
        ('투자의사 결정 스스로 내려본 경험 없음', '투자의사 결정 스스로 내려본 경험 없음'),
        ('주식과 채권, 예금과 적금을 구분할 수 있음', '주식과 채권, 예금과 적금을 구분할 수 있음'),
        ('투자할 수 있는 대부분의 금융상품 차이를 구별할 수 있음', '투자할 수 있는 대부분의 금융상품 차이를 구별할 수 있음'),
        ('금융상품과 투자대상 상품의 차이 이해할 수 있음', '금융상품과 투자대상 상품의 차이 이해할 수 있음'),
        ('Master', 'Master'),
    ]

    age_group = forms.ChoiceField(label='고객님의 연령대는 어떻게 되시나요?', choices=AGE_GROUP_CHOICES, widget=forms.RadioSelect)
    asset_ratio = forms.ChoiceField(label='총 자산대비 금융자산의 비중은 어느 정도 입니까?', choices=ASSET_RATIO_CHOICES, widget=forms.RadioSelect)
    expected_return = forms.ChoiceField(label='투자를 통해 기대하는 수익과 감내할 수 있는 손실은 어느 정도 입니까?', choices=EXPECTED_RETURN_CHOICES, widget=forms.RadioSelect)
    financial_knowledge = forms.ChoiceField(label='금융 상품에 대한 본인의 지식수준은 어느정도라고 생각하나요?', choices=FINANCIAL_KNOWLEDGE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = SurveyResponse
        fields = ['age_group', 'asset_ratio', 'expected_return', 'financial_knowledge']
