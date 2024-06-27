from airflow.operators.python import PythonOperator

import pendulum
from airflow import DAG
from common.seoul_realtime_python_code import select_now_time_info,get_seoul_api_xml_ver2
from common.s3_xml_to_csv import get_s3_xml_to_dataframe
from common.send_rds import send_postgres
from airflow.models import Variable

var_value=Variable.get("seoul_real_time_api_key")
postgresql_value=Variable.get('conn_postgres')

with DAG(
    dag_id="seoul_real_time_project_ver2", ## airflow에들어왔을때 보이는 dag이름
    schedule="*/10 * * * *",
    start_date=pendulum.datetime(2024, 2, 1, tz="Asia/Seoul"), ## 서울로설정
    catchup=False ## 날짜 누락된 구간은 코드 실행x(start_date부터 어제까지의 구간은 코드실행X) 
) as dag:
    
    
    select_now_time_info=PythonOperator(
        task_id='select_now_time_info',
        python_callable=select_now_time_info
    ) 
    
    get_seoul_api_xml_ver2=PythonOperator(
        task_id='get_seoul_api_xml_ver2',
        python_callable=get_seoul_api_xml_ver2,
        op_kwargs={'api_key':var_value}
    )
    
    get_s3_xml_to_dataframe=PythonOperator(
        task_id='get_s3_xml_to_dataframe',
        python_callable=get_s3_xml_to_dataframe
    )
    
    send_postgres=PythonOperator(
        task_id='send_postgres',
        python_callable=send_postgres,
        op_kwargs={'postgresql_conn':postgresql_value}
    )



select_now_time_info >> get_seoul_api_xml_ver2  >> get_s3_xml_to_dataframe >> send_postgres