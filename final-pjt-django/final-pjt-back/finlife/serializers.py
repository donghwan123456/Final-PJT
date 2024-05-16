from rest_framework import serializers
from .models import DepositProducts, DepositOptions

# serializers.Serializer
#   - 모델 필드에는 없어도 추가로 변환
# serailizers.ModelSerializer
#   - 모델 필드에 정의된 데이터만 변환

class DepositProductsSerializer(serializers.ModelSerializer):
    상품코드 = serializers.CharField(source='fin_prdt_cd')
    한국회사명 = serializers.CharField(source='kor_co_nm')
    금융상품명 = serializers.CharField(source='fin_prdt_nm')
    기타메모 = serializers.CharField(source='etc_note')
    가입거절여부 = serializers.IntegerField(source='join_deny')
    가입멤버 = serializers.CharField(source='join_member')
    가입방법 = serializers.CharField(source='join_way')

    class Meta:
        model = DepositProducts
        fields = ('상품코드', '한국회사명', '금융상품명', '기타메모', '가입거절여부', '가입멤버', '가입방법')


class DepositOptionsSerializer(serializers.ModelSerializer):
    상품 = serializers.PrimaryKeyRelatedField(queryset=DepositProducts.objects.all())
    상품코드 = serializers.CharField(source='fin_prdt_cd')
    이자유형명 = serializers.CharField(source='intr_rate_type_nm')
    이자율 = serializers.FloatField(source='intr_rate')
    이자율2 = serializers.FloatField(source='intr_rate2')
    저축기간 = serializers.IntegerField(source='save_trm')

    class Meta:
        model = DepositOptions
        fields = ('상품', '상품코드', '이자유형명', '이자율', '이자율2', '저축기간')

