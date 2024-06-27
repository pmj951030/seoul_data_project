from django.urls import path
from realtime_data.views import df_event_stts_veiws,df_fcst_ppltn_views,df_fcst12hours_views,df_fcst24hours_views,df_live_ppltn_stts_views,df_weather_stts_views

app_name='서울실시간데이터'

urlpatterns=[
    path('행사정보',df_event_stts_veiws.as_view(),name='행사정보'),
    path('시간별인구예상',df_fcst_ppltn_views.as_view(),name='시간별인구예상'),
    path('시간별예상날씨12',df_fcst12hours_views.as_view(),name='시간별예상날씨12'),
    path('시간별예상날씨24',df_fcst24hours_views.as_view(),name='시간별예상날씨24'),
    path('실시간인구현황',df_live_ppltn_stts_views.as_view(),name='실시간인구현황'),
    path('실시간날씨',df_weather_stts_views.as_view(),name='실시간날씨'),
]