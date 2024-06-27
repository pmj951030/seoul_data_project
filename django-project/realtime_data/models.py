from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from simple_history.models import HistoricalRecords
from django.utils import timezone
# Create your models here.
import re ## 정규표현식
from django.utils.translation import gettext_lazy as _ ## log추적할때

## admin_id
class admin_id(AbstractUser):
    pass ## 그냥 있는거 전부다 쓸꺼면 pass, 추가적으로 쓸꺼면 pass 지우고 다른 models.필드 만들기

## 행사정보
class df_event_stts(models.Model):
    
    file_id = models.CharField(blank=True,null=True,max_length=100,verbose_name="수집시간")
    AREA_CD = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 코드명")
    AREA_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 장소명")
    EVENT_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="문화행사명")
    EVENT_PERIOD = models.CharField(blank=True,null=True,max_length=100,verbose_name="문화행사 기간")
    EVENT_PLACE = models.CharField(blank=True,null=True,max_length=100,verbose_name="문화행사 장소")
    EVENT_ETC_DETAIL = models.CharField(blank=True,null=True,max_length=100,verbose_name="문화행사 기타 세부정보")
    EVENT_X = models.CharField(blank=True,null=True,max_length=100,verbose_name="X좌표")
    EVENT_Y = models.CharField(blank=True,null=True,max_length=100,verbose_name="Y좌표")

    history = HistoricalRecords()  # HistoricalRecords 필드 추가
    def __str__(self):
        return f"{self.file_id} {self.AREA_NM}"
    class Meta:
        verbose_name_plural = "01.행사정보"
        
## 시간별 인구 예상
class df_fcst_ppltn(models.Model):

    file_id = models.CharField(blank=True,null=True,max_length=100,verbose_name="수집시간")
    AREA_CD = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 코드명")
    AREA_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 장소명")
    FCST_TIME = models.CharField(blank=True,null=True,max_length=100,verbose_name="예측시점")
    FCST_CONGEST_LVL = models.CharField(blank=True,null=True,max_length=100,verbose_name="장소 예측 혼잡도 지표")
    FCST_PPLTN_MIN = models.DecimalField(max_digits=12, decimal_places=0,verbose_name="예측 실시간 인구 지표 최소값")
    FCST_PPLTN_MAX = models.DecimalField(max_digits=12, decimal_places=0,verbose_name="예측 실시간 인구 지표 최대값")


    history = HistoricalRecords()  # HistoricalRecords 필드 추가
    def __str__(self):
        return f"{self.file_id} {self.AREA_NM}"
    class Meta:
        verbose_name_plural = "02.시간별 인구 예상"
        
## 시간별 예상 날씨(12시간)
class df_fcst12hours(models.Model):
    file_id = models.CharField(blank=True,null=True,max_length=100,verbose_name="수집시간")
    AREA_CD = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 코드명")
    AREA_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 장소명")
    FCST_DT = models.CharField(blank=True,null=True,max_length=100,verbose_name="예보시간")
    TEMP = models.CharField(blank=True,null=True,max_length=100,verbose_name="기온")
    PRECIPITATION = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수량")
    PRECPT_TYPE = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수형태")
    RAIN_CHANCE = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수확률")
    SKY_STTS = models.CharField(blank=True,null=True,max_length=100,verbose_name="하늘상태")
    FCST_TIME = models.CharField(blank=True,null=True,max_length=100,verbose_name="예측시점")

    history = HistoricalRecords()  # HistoricalRecords 필드 추가
    def __str__(self):
        return f"{self.file_id} {self.AREA_NM}"
    class Meta:
        verbose_name_plural = "03.시간별 예상 날씨(12시간)"
        
## 시간별 예상 날씨(24시간)
class df_fcst24hours(models.Model):
    
    file_id = models.CharField(blank=True,null=True,max_length=100,verbose_name="수집시간")
    AREA_CD = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 코드명")
    AREA_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 장소명")
    FCST_DT = models.CharField(blank=True,null=True,max_length=100,verbose_name="예보시간")
    TEMP = models.CharField(blank=True,null=True,max_length=100,verbose_name="기온")
    PRECIPITATION = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수량")
    PRECPT_TYPE = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수형태")
    RAIN_CHANCE = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수확률")
    SKY_STTS = models.CharField(blank=True,null=True,max_length=100,verbose_name="하늘상태")

    history = HistoricalRecords()  # HistoricalRecords 필드 추가
    def __str__(self):
        return f"{self.file_id} {self.AREA_NM}"
    class Meta:
        verbose_name_plural = "04.시간별 예상 날씨(24시간)"
        
## 실시간인구현황
class df_live_ppltn_stts(models.Model):
    
    file_id = models.CharField(blank=True,null=True,max_length=100,verbose_name="수집시간")
    AREA_CD = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 코드명")
    AREA_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 장소명")
    AREA_CONGEST_LVL = models.CharField(blank=True,null=True,max_length=100,verbose_name="장소 혼잡도 지표")
    AREA_CONGEST_MSG = models.CharField(blank=True,null=True,max_length=100,verbose_name="장소 혼잡도 지표 관련 메세지")
    AREA_PPLTN_MIN = models.CharField(blank=True,null=True,max_length=100,verbose_name="실시간 인구 지표 최소값")
    AREA_PPLTN_MAX = models.CharField(blank=True,null=True,max_length=100,verbose_name="실시간 인구 지표 최대값")
    MALE_PPLTN_RATE = models.CharField(blank=True,null=True,max_length=100,verbose_name="남성 인구 비율(남성)")
    FEMALE_PPLTN_RATE = models.CharField(blank=True,null=True,max_length=100,verbose_name="여성 인구 비율(여성)")
    PPLTN_RATE_0 = models.CharField(blank=True,null=True,max_length=100,verbose_name="0~10세 인구 비율")
    PPLTN_RATE_10 = models.CharField(blank=True,null=True,max_length=100,verbose_name="10대 실시간 인구 비율")
    PPLTN_RATE_20 = models.CharField(blank=True,null=True,max_length=100,verbose_name="20대 실시간 인구 비율")
    PPLTN_RATE_30 = models.CharField(blank=True,null=True,max_length=100,verbose_name="30대 실시간 인구 비율")
    PPLTN_RATE_40 = models.CharField(blank=True,null=True,max_length=100,verbose_name="40대 실시간 인구 비율")
    PPLTN_RATE_50 = models.CharField(blank=True,null=True,max_length=100,verbose_name="50대 실시간 인구 비율")
    PPLTN_RATE_60 = models.CharField(blank=True,null=True,max_length=100,verbose_name="60대 실시간 인구 비율")
    PPLTN_RATE_70 = models.CharField(blank=True,null=True,max_length=100,verbose_name="70대 실시간 인구 비율")
    RESNT_PPLTN_RATE = models.CharField(blank=True,null=True,max_length=100,verbose_name="상주 인구 비율")
    NON_RESNT_PPLTN_RATE = models.CharField(blank=True,null=True,max_length=100,verbose_name="비상주 인구 비율")
    REPLACE_YN = models.CharField(blank=True,null=True,max_length=100,verbose_name="대체 데이터 여부")
    PPLTN_TIME = models.CharField(blank=True,null=True,max_length=100,verbose_name="실시간 인구 데이터 업데이트 시간")
    FCST_YN = models.CharField(blank=True,null=True,max_length=100,verbose_name="예측값 제공 여부")
    # FCST_PPLTN = models.CharField(blank=True,null=True,max_length=100,verbose_name="인구 예측 오브젝트")
    FCST_PPLTN = models.TextField(blank=True,null=True,verbose_name="인구 예측 오브젝트")
    history = HistoricalRecords()  # HistoricalRecords 필드 추가
    def __str__(self):
        return f"{self.file_id} {self.AREA_NM}"
    class Meta:
        verbose_name_plural = "05.실시간인구현황"
        
## 실시간 날씨
class df_weather_stts(models.Model):

    file_id = models.CharField(blank=True,null=True,max_length=100,verbose_name="수집시간")
    AREA_CD = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 코드명")
    AREA_NM = models.CharField(blank=True,null=True,max_length=100,verbose_name="핫스팟 장소명")
    WEATHER_TIME = models.CharField(blank=True,null=True,max_length=100,verbose_name="날씨 데이터 업데이트 시간")
    TEMP = models.CharField(blank=True,null=True,max_length=100,verbose_name="기온")
    SENSIBLE_TEMP = models.CharField(blank=True,null=True,max_length=100,verbose_name="체감온도")
    MAX_TEMP = models.CharField(blank=True,null=True,max_length=100,verbose_name="일 최고온도")
    MIN_TEMP = models.CharField(blank=True,null=True,max_length=100,verbose_name="일 최저온도")
    HUMIDITY = models.CharField(blank=True,null=True,max_length=100,verbose_name="습도")
    WIND_DIRCT = models.CharField(blank=True,null=True,max_length=100,verbose_name="풍향")
    WIND_SPD = models.CharField(blank=True,null=True,max_length=100,verbose_name="풍속")
    PRECIPITATION = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수량")
    PRECPT_TYPE = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수형태")
    # PCP_MSG = models.CharField(blank=True,null=True,max_length=100,verbose_name="강수관련 메세지")
    PCP_MSG = models.TextField(blank=True,null=True,verbose_name="강수관련 메세지")
    SUNRISE = models.CharField(blank=True,null=True,max_length=100,verbose_name="일출시각")
    SUNSET = models.CharField(blank=True,null=True,max_length=100,verbose_name="일몰시각")
    UV_INDEX_LVL = models.CharField(blank=True,null=True,max_length=100,verbose_name="자외선지수 단계")
    UV_INDEX = models.CharField(blank=True,null=True,max_length=100,verbose_name="자외선지수")
    # UV_MSG = models.CharField(blank=True,null=True,max_length=100,verbose_name="자외선메세지")
    UV_MSG = models.TextField(blank=True,null=True,verbose_name="자외선메세지")
    PM25_INDEX = models.CharField(blank=True,null=True,max_length=100,verbose_name="초미세먼지지표")
    PM25 = models.CharField(blank=True,null=True,max_length=100,verbose_name="초미세먼지농도")
    PM10_INDEX = models.CharField(blank=True,null=True,max_length=100,verbose_name="미세먼지지표")
    PM10 = models.CharField(blank=True,null=True,max_length=100,verbose_name="미세먼지농도")
    AIR_IDX = models.CharField(blank=True,null=True,max_length=100,verbose_name="통합대기환경등급")
    AIR_IDX_MVL = models.CharField(blank=True,null=True,max_length=100,verbose_name="통합대기환경지수")
    AIR_IDX_MAIN = models.CharField(blank=True,null=True,max_length=100,verbose_name="통합대기환경지수 결정물질")
    # AIR_MSG = models.CharField(blank=True,null=True,max_length=100,verbose_name="통합대기환경등급별 메세지")
    AIR_MSG = models.TextField(blank=True,null=True,verbose_name="통합대기환경등급별 메세지")
    # FCST24HOURS = models.CharField(blank=True,null=True,max_length=100,verbose_name="날씨 데이터 업데이트 시간")
    FCST24HOURS = models.TextField(blank=True,null=True,verbose_name="날씨 데이터 업데이트 시간")
    # NEWS_LIST = models.CharField(blank=True,null=True,max_length=100,verbose_name="기상관련특보")
    NEWS_LIST = models.TextField(blank=True,null=True,verbose_name="기상관련특보")

    history = HistoricalRecords()  # HistoricalRecords 필드 추가
    def __str__(self):
        return f"{self.file_id} {self.AREA_NM}"
    class Meta:
        verbose_name_plural = "06.실시간 날씨"