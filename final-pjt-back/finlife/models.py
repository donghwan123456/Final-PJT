from django.db import models

# Create your models here.
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_note = models.TextField()
    join_deny = models.IntegerField()
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()
    max_limit = models.IntegerField(default=0)


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    save_trm = models.IntegerField()


class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField()      # 금융 회사명
    fin_prdt_nm = models.TextField()    # 금융 상품명
    etc_note = models.TextField()       # 기타 유의사항
    join_deny = models.IntegerField()   # 가입 제한
    join_member = models.TextField()   # 가입 대상
    join_way = models.TextField()   # 가입방법
    spcl_cnd = models.TextField()   # 우대조건
    max_limit = models.IntegerField(default=0) # 최고한도


class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100) # 저축 금리 유형명
    intr_rate = models.FloatField()     # 저축 금리
    intr_rate2 = models.FloatField()    # 최고 우대 금리
    save_trm = models.IntegerField() # 저축 기간
    rsrv_type = models.TextField() # 적립 유형
    rsrv_type_nm = models.TextField() # 적립 유형명
