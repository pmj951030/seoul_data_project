import pandas as pd
from sqlalchemy import create_engine,text
# from airflow.hooks.postgres_hook import PostgresHook
# from airflow.providers.postgres.hooks.postgres import PostgresHook

def send_postgres(postgresql_conn,**kwargs):  
    ## 행사정보
    try:
        df_event_stts=pd.read_csv('files/df_event_stts.csv')
        postgres_conn_str=postgresql_conn
        engine = create_engine(postgres_conn_str)
        table_exists_query = text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'realtime_data_df_event_stts')")
        table_exists = engine.execute(table_exists_query).scalar()
        if not table_exists:
            df_event_stts.to_sql('realtime_data_df_event_stts', engine, if_exists='replace', index=False)
        else:
            # 테이블이 있으면 데이터 추가
            df_event_stts.to_sql('realtime_data_df_event_stts', engine, if_exists='append', index=False)
        # return df_event_stts
    except:
        pass
    
    ## 시간별 인구 예상
    try:
        df_fcst_ppltn=pd.read_csv('files/df_fcst_ppltn.csv')
        postgres_conn_str=postgresql_conn
        engine = create_engine(postgres_conn_str)
        table_exists_query = text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'realtime_data_df_fcst_ppltn')")
        table_exists = engine.execute(table_exists_query).scalar()
        if not table_exists:
            df_fcst_ppltn.to_sql('realtime_data_df_fcst_ppltn', engine, if_exists='replace', index=False)
        else:
            # 테이블이 있으면 데이터 추가
            df_fcst_ppltn.to_sql('realtime_data_df_fcst_ppltn', engine, if_exists='append', index=False)
        # return df_fcst_ppltn
    except:
        pass
    
    ## 시간별 예상 날씨(12시간)
    try:
        df_fcst12hours=pd.read_csv('files/df_fcst12hours.csv')
        postgres_conn_str=postgresql_conn
        engine = create_engine(postgres_conn_str)
        table_exists_query = text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'realtime_data_df_fcst12hours')")
        table_exists = engine.execute(table_exists_query).scalar()
        if not table_exists:
            df_fcst12hours.to_sql('realtime_data_df_fcst12hours', engine, if_exists='replace', index=False)
        else:
            # 테이블이 있으면 데이터 추가
            df_fcst12hours.to_sql('realtime_data_df_fcst12hours', engine, if_exists='append', index=False)
        # return df_fcst12hours
    except:
        pass

    ## 시간별 예상 날씨(24시간)
    try:
        df_fcst24hours=pd.read_csv('files/df_fcst24hours.csv')
        postgres_conn_str=postgresql_conn
        engine = create_engine(postgres_conn_str)
        table_exists_query = text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'realtime_data_df_fcst24hours')")
        table_exists = engine.execute(table_exists_query).scalar()
        if not table_exists:
            df_fcst24hours.to_sql('realtime_data_df_fcst24hours', engine, if_exists='replace', index=False)
        else:
            # 테이블이 있으면 데이터 추가
            df_fcst24hours.to_sql('realtime_data_df_fcst24hours', engine, if_exists='append', index=False)
        # return df_fcst24hours
    except:
        pass
    
    ## 실시간인구현황
    try:
        df_live_ppltn_stts=pd.read_csv('files/df_live_ppltn_stts.csv')
        postgres_conn_str=postgresql_conn
        engine = create_engine(postgres_conn_str)
        table_exists_query = text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'realtime_data_df_live_ppltn_stts')")
        table_exists = engine.execute(table_exists_query).scalar()
        if not table_exists:
            df_live_ppltn_stts.to_sql('realtime_data_df_live_ppltn_stts', engine, if_exists='replace', index=False)
        else:
            # 테이블이 있으면 데이터 추가
            df_live_ppltn_stts.to_sql('realtime_data_df_live_ppltn_stts', engine, if_exists='append', index=False)

    except:
        pass
    
    ## 실시간 날씨
    try:
        df_weather_stts=pd.read_csv('files/df_weather_stts.csv')
        postgres_conn_str=postgresql_conn
        engine = create_engine(postgres_conn_str)
        table_exists_query = text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'realtime_data_df_weather_stts')")
        table_exists = engine.execute(table_exists_query).scalar()
        if not table_exists:
            df_weather_stts.to_sql('realtime_data_df_weather_stts', engine, if_exists='replace', index=False)
        else:
            # 테이블이 있으면 데이터 추가
            df_weather_stts.to_sql('realtime_data_df_weather_stts', engine, if_exists='append', index=False)

    except:
        pass