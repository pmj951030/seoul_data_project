import requests
import datetime
from pytz import timezone
import pandas as pd
import json
import xmltodict
import boto3
from airflow.providers.amazon.aws.hooks.s3 import S3Hook 

list_subway_2line=[ 'POI014','POI015','POI018','POI019',
                    'POI023','POI025','POI029','POI031',
                    'POI034','POI039','POI040','POI042',
                    'POI045','POI052','POI053','POI055']


def select_now_time_info(**kwargs): ## 파일명에 쓸있도록 날짜, 시간 가져오기
    code_start_time=datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S') ## 파일명에 사용
    return code_start_time

        
def get_seoul_api_xml_ver2(api_key,**kwargs):## xml 수집해서 s3에 저장
    code_start_time = kwargs['task_instance'].xcom_pull(task_ids='select_now_time_info')
    hook = S3Hook('seoul-realtime-xml-key')
    bucket_name = 'seoul-realtime-xml' 
    
    for input_location in list_subway_2line:
        response = requests.get(f'http://openapi.seoul.go.kr:8088/{api_key}/xml/citydata/1/5/{input_location}', stream=True)
        parsed_dict = xmltodict.parse(response.text)
        json_data = json.dumps(parsed_dict)

        key = f'source_data_xmldict/source_{input_location}_{code_start_time}.xml'
        hook.load_string(json_data, key, bucket_name, replace=True)


