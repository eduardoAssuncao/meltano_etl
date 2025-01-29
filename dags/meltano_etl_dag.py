from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'meltano_etl_dag',
    default_args=default_args,
    description='DAG para extrair dados do PostgreSQL para CSV e carregar em outro PostgreSQL usando Meltano',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

def run_meltano_extract():
    process = subprocess.Popen(
        'meltano run tap-postgres target-csv',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    print("TESTE TESTE TESTE TESTE")
    # print("STDOUT:", stdout.decode())
    # print("STDERR:", stderr.decode())

def run_meltano_load():
    process = subprocess.Popen(
        'meltano run tap-csv target-postgres',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    print("STDOUT:", stdout.decode())
    print("STDERR:", stderr.decode())

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=run_meltano_extract,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=run_meltano_load,
    dag=dag,
)

extract_task >> load_task
