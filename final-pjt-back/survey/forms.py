from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    ASSET_RATIO_CHOICES = [
        ('5% 이하', '5% 이하'),
        ('10% 이하', '10% 이하'),
        ('20% 이하', '20% 이하'),
        ('30% 이하', '30% 이하'),
        ('30% 초과', '30% 초과'),
    ]

    EXPECTED_RETURN_CHOICES = [
        ('원금 보존이 무조건!', '원금 보존이 무조건!'),
        ('예적금 수익률보다 3% 이상 기대 가능하다면 원금보존 가능성이 조금 낮아져도 괜찮다', '예적금 수익률보다 3% 이상 기대 가능하다면 원금보존 가능성이 조금 낮아져도 괜찮다'),
        ('High Risk - High Return', 'High Risk - High Return'),
    ]

    FINANCIAL_KNOWLEDGE_CHOICES = [
        ('투자의사 결정 스스로 내려본 경험 없음', '투자의사 결정 스스로 내려본 경험 없음'),
        ('주식과 채권, 예금과 적금을 구분할 수 있음', '주식과 채권, 예금과 적금을 구분할 수 있음'),
        ('투자할 수 있는 대부분의 금융상품 차이를 구별할 수 있음', '투자할 수 있는 대부분의 금융상품 차이를 구별할 수 있음'),
        ('금융상품과 투자대상 상품의 차이 이해할 수 있음', '금융상품과 투자대상 상품의 차이 이해할 수 있음'),
        ('Master', 'Master'),
    ]

    age = forms.IntegerField(
        label='고객님의 나이는 어떻게 되시나요?',
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        widget=forms.NumberInput(attrs={'min': '0', 'max': '120'})
    )
    asset_ratio = forms.ChoiceField(label='총 자산대비 금융자산의 비중은 어느 정도 입니까?', choices=ASSET_RATIO_CHOICES, widget=forms.RadioSelect)
    expected_return = forms.ChoiceField(label='투자를 통해 기대하는 수익과 감내할 수 있는 손실은 어느 정도 입니까?', choices=EXPECTED_RETURN_CHOICES, widget=forms.RadioSelect)
    financial_knowledge = forms.ChoiceField(label='금융 상품에 대한 본인의 지식수준은 어느정도라고 생각하나요?', choices=FINANCIAL_KNOWLEDGE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = SurveyResponse
        fields = ['age', 'asset_ratio', 'expected_return', 'financial_knowledge']
