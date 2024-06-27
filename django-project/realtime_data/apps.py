from django.apps import AppConfig


class RealtimeDataConfig(AppConfig):
    name = 'realtime_data'
    default_auto_field = 'django.db.models.AutoField' ## 자동생성되는 키를 기본키로 했을때 경고메세지 뜨는데 그거 안뜨게함