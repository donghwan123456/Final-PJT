from django.db import models

# Create your models here.
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(verbose_name="상품코드", unique=True)
    kor_co_nm = models.TextField(verbose_name="금융 회사명")
    fin_prdt_nm = models.TextField(verbose_name="금융 상품명")
    etc_note = models.TextField(verbose_name="기타 메모")
    join_deny = models.IntegerField(verbose_name="가입 제한")
    join_member = models.TextField(verbose_name="가입 대상")
    join_way = models.TextField(verbose_name="가입 방법")
    max_limit = models.IntegerField(verbose_name="최고 한도")
    # spcl_cnd = models.TextField()


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField(verbose_name="상품 코드")
    intr_rate_type_nm = models.CharField(max_length=100, verbose_name="저축 금리 유형명")
    intr_rate = models.FloatField(verbose_name="저축 금리")
    intr_rate2 = models.FloatField(verbose_name="최고 우대금리")
    save_trm = models.IntegerField(verbose_name="저축 기간")
