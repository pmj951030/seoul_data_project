# import requests
# import datetime
# from pytz import timezone
import pandas as pd
import json
# import xmltodict
import boto3
from airflow.providers.amazon.aws.hooks.s3 import S3Hook 

## xml가져와서 필요한부분만 바꾸고 df로 수정
def get_s3_xml_to_dataframe(**kwargs):
    ## 2호선 라인
    list_subway_2line=[ 'POI014','POI015','POI018','POI019',
                        'POI023','POI025','POI029','POI031',
                        'POI034','POI039','POI040','POI042',
                        'POI045','POI052','POI053','POI055']
    code_start_time = kwargs['task_instance'].xcom_pull(task_ids='select_now_time_info')
    
    ## s3 가져오는거 세팅
    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    aws_credentials = hook.get_credentials()# S3 클라이언트 생성
    # Boto3를 사용하여 AWS 자격 증명을 설정
    session = boto3.Session(
        aws_access_key_id=aws_credentials.access_key,
        aws_secret_access_key=aws_credentials.secret_key,
        region_name='ap-northeast-2')
    s3_client = session.client('s3') # 이제 session 객체를 사용하여 AWS 리소스 또는 서비스에 액세스할 수 있음
    bucket_name = 'seoul-realtime-xml' ## 데이터 가져올 버킷
    
    ## 빈 데이터프레임만들기 (여기에 지역정보들 통합해서 넣을 예정)
    df_live_ppltn_stts=pd.DataFrame()
    df_fcst_ppltn=pd.DataFrame()
    df_weather_stts=pd.DataFrame()
    df_fcst24hours=pd.DataFrame()
    df_fcst12hours=pd.DataFrame()
    df_event_stts=pd.DataFrame()
    
    
    
    ## 파일명 리스트 가져오기
    folder_path = 'source_data_xmldict/'
    response = s3_client.list_objects_v2(Bucket=bucket_name,Prefix=folder_path)
    # list_files = [obj['Key'] for obj in response['Contents']][1:] ## [0]은 source_data_xmldict/까지 출력됨
    list_files=[]
    if 'Contents' in response:
        for obj in response['Contents'][1:]:
            list_files.append(obj['Key'])

    # 다음 페이지가 있는지 확인하고 요청을 보냄
    while response.get('NextContinuationToken'):
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path, ContinuationToken=response['NextContinuationToken'])
        for obj in response['Contents'][1:]:
            list_files.append(obj['Key'])
    
    
    # 파일명 리스트 생성
    ## 현재 2호선데이터만 이미 다운로드 받아서 크게 상관없지만 향후 특정 지역 제외해서 집계하는 경우가 생길 수 있으므로 사용
    valid_file_names = []
    for file_path in list_files:
        for substring in list_subway_2line:
            if substring in file_path:
                valid_file_names.append(file_path.split('/')[-1])
                break    
    
    specific_word = code_start_time ## 여기에 날짜 뭐넣을지 반복문 사용 예정

    # 특정 단어가 포함된 파일명 리스트 생성
    ## 특정날짜_시간에 해당하는 파일들 전부 가져오기
    """['source_POI025_20240302_154704.xml',...,'source_POI029_20240302_154704.xml']"""
    select_date_file = [file_path for file_path in valid_file_names if specific_word in file_path]
    
    for input_date in select_date_file:
        input_file_path=f'source_data_xmldict/{input_date}'
        response = s3_client.get_object(Bucket=bucket_name, Key=input_file_path)
        json_data = response['Body'].read().decode('utf-8')
        parsed_dict = json.loads(json_data)
        base_xml=parsed_dict['SeoulRtd.citydata']['CITYDATA']
        area_cd=base_xml['AREA_CD'] ## 핫스팟 코드명
        area_nm=base_xml['AREA_NM'] ## 핫스팟 장소명
        ## 실시간인구현황
        try:
            live_ppltn_stts=base_xml['LIVE_PPLTN_STTS']['LIVE_PPLTN_STTS']  
            sample_df_live_ppltn_stts=pd.DataFrame([live_ppltn_stts])
            sample_df_live_ppltn_stts.insert(loc=0, column='file_id', value=code_start_time)
            sample_df_live_ppltn_stts.insert(loc=1, column='AREA_CD', value=area_cd)
            sample_df_live_ppltn_stts.insert(loc=2, column='AREA_NM', value=area_nm)
            df_live_ppltn_stts = pd.concat([df_live_ppltn_stts, sample_df_live_ppltn_stts], ignore_index=True)
        except:
            pass
        ## 시간별 인구 예상, 이 데이터 없는 지역도있음
        try:
            sample_df_fcst_ppltn=pd.DataFrame(live_ppltn_stts['FCST_PPLTN']['FCST_PPLTN'])
            sample_df_fcst_ppltn.insert(loc=0, column='file_id', value=code_start_time)
            sample_df_fcst_ppltn.insert(loc=1, column='AREA_CD', value=area_cd)
            sample_df_fcst_ppltn.insert(loc=2, column='AREA_NM', value=area_nm)
            df_fcst_ppltn = pd.concat([df_fcst_ppltn, sample_df_fcst_ppltn], ignore_index=True)
        except:
            pass
    
        ## 실시간 날씨
        try:
            sample_df_weather_stts=pd.DataFrame(base_xml['WEATHER_STTS']['WEATHER_STTS']) 
            sample_df_weather_stts.insert(loc=0, column='file_id', value=code_start_time)
            sample_df_weather_stts.insert(loc=1, column='AREA_CD', value=area_cd)
            sample_df_weather_stts.insert(loc=2, column='AREA_NM', value=area_nm)
            df_weather_stts = pd.concat([df_weather_stts, sample_df_weather_stts], ignore_index=True)
        except:
            pass    
        
        ## 시간별 예상 날씨(24시간)
        try:
            sample_df_fcst24hours=pd.DataFrame(base_xml['WEATHER_STTS']['WEATHER_STTS']['FCST24HOURS']['FCST24HOURS'])
            sample_df_fcst24hours.insert(loc=0, column='file_id', value=code_start_time)
            sample_df_fcst24hours.insert(loc=1, column='AREA_CD', value=area_cd)
            sample_df_fcst24hours.insert(loc=2, column='AREA_NM', value=area_nm)
            df_fcst24hours = pd.concat([df_fcst24hours, sample_df_fcst24hours], ignore_index=True)
        except:
            pass
        

        
        ## 행사정보
        try: ## 2개이상
            sample_df_event_stts=pd.DataFrame(base_xml['EVENT_STTS']['EVENT_STTS'])
            sample_df_event_stts.insert(loc=0, column='file_id', value=code_start_time)
            sample_df_event_stts.insert(loc=1, column='AREA_CD', value=area_cd)
            sample_df_event_stts.insert(loc=2, column='AREA_NM', value=area_nm)
            df_event_stts = pd.concat([df_event_stts, sample_df_event_stts], ignore_index=True)
        except:
            try: ## 1개
                sample_df_event_stts=pd.DataFrame([base_xml['EVENT_STTS']['EVENT_STTS']])
                sample_df_event_stts.insert(loc=0, column='file_id', value=code_start_time)
                sample_df_event_stts.insert(loc=1, column='AREA_CD', value=area_cd)
                sample_df_event_stts.insert(loc=2, column='AREA_NM', value=area_nm)
                df_event_stts = pd.concat([df_event_stts, sample_df_event_stts], ignore_index=True)
            except: ## 없음
                pass

        
    #####s3에 저장
    ## 실시간인구현황
    df_live_ppltn_stts.reset_index(drop=True,inplace=True)
    save_local_path_df_live_ppltn_stts='files/df_live_ppltn_stts.csv'
    save_s3_path_df_live_ppltn_stts=f'xml_to_csv_data/live_ppltn_stts_fold/df_live_ppltn_stts_{code_start_time}.csv'
    df_live_ppltn_stts.to_csv(save_local_path_df_live_ppltn_stts,index=False)

    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    hook.load_file(
        filename=save_local_path_df_live_ppltn_stts,
        key=save_s3_path_df_live_ppltn_stts,
        bucket_name=bucket_name,
        replace=True  # 파일이 이미 존재하는 경우 덮어쓸지 여부를 결정합니다.
    )
    
    ## 시간별 인구 예상
    df_fcst_ppltn.reset_index(drop=True,inplace=True)
    save_local_path_df_fcst_ppltn='files/df_fcst_ppltn.csv'
    save_s3_path_df_fcst_ppltn=f'xml_to_csv_data/fcst_ppltn_fold/df_fcst_ppltn_{code_start_time}.csv'
    df_fcst_ppltn.to_csv(save_local_path_df_fcst_ppltn,index=False)

    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    hook.load_file(
        filename=save_local_path_df_fcst_ppltn,
        key=save_s3_path_df_fcst_ppltn,
        bucket_name=bucket_name,
        replace=True  # 파일이 이미 존재하는 경우 덮어쓸지 여부를 결정합니다.
    )
    
    ## 실시간 날씨
    df_weather_stts.reset_index(drop=True,inplace=True)
    save_local_path_df_weather_sttsn='files/df_weather_stts.csv'
    save_s3_path_df_weather_stts=f'xml_to_csv_data/weather_stts_fold/df_weather_stts_{code_start_time}.csv'
    df_weather_stts.to_csv(save_local_path_df_weather_sttsn,index=False)

    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    hook.load_file(
        filename=save_local_path_df_weather_sttsn,
        key=save_s3_path_df_weather_stts,
        bucket_name=bucket_name,
        replace=True  # 파일이 이미 존재하는 경우 덮어쓸지 여부를 결정합니다.
    )
    
    ## 실시간 예상 날씨 24시간
    df_fcst24hours.reset_index(drop=True,inplace=True)
    save_local_path_df_fcst24hour='files/df_fcst24hours.csv'
    save_s3_path_df_fcst24hour=f'xml_to_csv_data/fcst24hours_fold/df_fcst24hours_{code_start_time}.csv'
    df_fcst24hours.to_csv(save_local_path_df_fcst24hour,index=False)

    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    hook.load_file(
        filename=save_local_path_df_fcst24hour,
        key=save_s3_path_df_fcst24hour,
        bucket_name=bucket_name,
        replace=True  # 파일이 이미 존재하는 경우 덮어쓸지 여부를 결정합니다.
    )
    

    
    ## 행사정보
    df_event_stts.reset_index(drop=True,inplace=True)
    save_local_path_df_event_stts='files/df_event_stts.csv'
    save_s3_path_df_event_stts=f'xml_to_csv_data/event_stts_fold/df_event_stts_{code_start_time}.csv'
    df_event_stts.to_csv(save_local_path_df_event_stts,index=False)

    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    hook.load_file(
        filename=save_local_path_df_event_stts,
        key=save_s3_path_df_event_stts,
        bucket_name=bucket_name,
        replace=True  # 파일이 이미 존재하는 경우 덮어쓸지 여부를 결정합니다.
    )
    
    
    ## 시간별 예상 날씨(12시간)
    df_fcst_ppltn=pd.read_csv('files/df_fcst_ppltn.csv')
    df_fcst24hours=pd.read_csv('files/df_fcst24hours.csv')
    select_time=list(pd.unique(df_fcst_ppltn['FCST_TIME']))
    df_fcst24hours['FCST_TIME']=df_fcst24hours['FCST_DT'].apply(lambda x : str(x)[0:4]+'-'+ \
                        str(x)[4:6].zfill(2)+'-'+ \
                        str(x)[6:8].zfill(2)+' '+ \
                            str(x)[8:10].zfill(2)+':'+\
                            str(x)[10:12].zfill(2))
    df_fcst12hours=df_fcst24hours[df_fcst24hours['FCST_TIME'].isin(select_time)]
        
    

    ## 실시간 예상 날씨 12시간 저장
    df_fcst12hours.reset_index(drop=True,inplace=True)
    save_local_path_df_fcst12hour='files/df_fcst12hours.csv'
    save_s3_path_df_fcst12hour=f'xml_to_csv_data/fcst12hours_fold/df_fcst12hours_{code_start_time}.csv'
    df_fcst12hours.to_csv(save_local_path_df_fcst12hour,index=False)

    hook = S3Hook('seoul-realtime-xml-key')  # your_s3_conn_id를 실제 연결 ID로 대체합니다.
    hook.load_file(
        filename=save_local_path_df_fcst12hour,
        key=save_s3_path_df_fcst12hour,
        bucket_name=bucket_name,
        replace=True  # 파일이 이미 존재하는 경우 덮어쓸지 여부를 결정합니다.
    )