from django.shortcuts import render
from django.db.models import Q
from realtime_data.models import df_event_stts,df_fcst_ppltn,df_fcst12hours,df_fcst24hours,df_live_ppltn_stts,df_weather_stts
from django.views import generic

# Create your views here.
class first_View(generic.TemplateView):
    template_name = "main_page.html"
    
## 행사정보
class df_event_stts_veiws(generic.ListView): ## 행사정보
    template_name = 'event_stts.html'
    queryset = df_event_stts.objects.all()
    paginate_by = 50 ## 한페이지에 볼수있는 데이터 수
    context_object_name= "key"
    
    ## 필터할때 사용
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            filter_conditions = Q()
            fields = ['AREA_NM','EVENT_NM','EVENT_PLACE','EVENT_ETC_DETAIL']
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
## 시간별인구예상
class df_fcst_ppltn_views(generic.ListView): ## 시간별인구예상
    template_name = 'fcst_ppltn.html'
    queryset = df_fcst_ppltn.objects.all()
    paginate_by = 50 ## 한페이지에 볼수있는 데이터 수
    context_object_name= "key"
    
    ## 필터할때 사용
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            filter_conditions = Q()
            fields = ['AREA_NM']
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
    
## 시간별 예상 날씨(12시간)
class df_fcst12hours_views(generic.ListView): ## 시간별인구예상
    template_name = 'fcst12hours.html'
    queryset = df_fcst12hours.objects.all()
    paginate_by = 50 ## 한페이지에 볼수있는 데이터 수
    context_object_name= "key"
    
    ## 필터할때 사용
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            filter_conditions = Q()
            fields = ['AREA_NM']
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
## 시간별 예상 날씨(24시간)
class df_fcst24hours_views(generic.ListView): ## 시간별인구예상
    template_name = 'fcst24hours.html'
    queryset = df_fcst24hours.objects.all()
    paginate_by = 50 ## 한페이지에 볼수있는 데이터 수
    context_object_name= "key"
    
    ## 필터할때 사용
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            filter_conditions = Q()
            fields = ['AREA_NM']
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
## 실시간인구현황
class df_live_ppltn_stts_views(generic.ListView): ## 시간별인구예상
    template_name = 'live_ppltn_stts.html'
    queryset = df_live_ppltn_stts.objects.all()
    paginate_by = 50 ## 한페이지에 볼수있는 데이터 수
    context_object_name= "key"
    
    ## 필터할때 사용
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            filter_conditions = Q()
            fields = ['AREA_NM']
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
## 실시간날씨
class df_weather_stts_views(generic.ListView): ## 시간별인구예상
    template_name = 'weather_stts.html'
    queryset = df_weather_stts.objects.all()
    paginate_by = 50 ## 한페이지에 볼수있는 데이터 수
    context_object_name= "key"
    
    ## 필터할때 사용
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            filter_conditions = Q()
            fields = ['AREA_NM']
            for field in fields:
                filter_conditions |= Q(**{f'{field}__icontains': search_query})

            queryset = queryset.filter(filter_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context