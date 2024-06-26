from rest_framework import serializers
from .models import DepositProducts, DepositOptions
from .models import SavingProducts, SavingOptions

# serializers.Serializer
#   - 모델 필드에는 없어도 추가로 변환
# serailizers.ModelSerializer
#   - 모델 필드에 정의된 데이터만 변환

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)
