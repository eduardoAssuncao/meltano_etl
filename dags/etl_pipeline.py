from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import psycopg2

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1), 
}

def extract_from_csv(**kwargs):
    df = pd.read_csv('/opt/airflow/dags/order_details_mock.csv')
    print("Colunas disponíveis no CSV:", df.columns.tolist())  
    return df.to_dict(orient='list') 

def load_to_postgres(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract_from_csv')
    df = pd.DataFrame(data)

    print("Colunas no DataFrame carregado:", df.columns.tolist())

  
    conn = psycopg2.connect(
        dbname="postgres", user="admin123", password="admin123", host="172.25.188.100", port="5432"
    )
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO orders (order_id, product_id, unit_price, quantity, discount)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                row.get('order_id'),  
                row.get('product_id'),
                row.get('unity_price'),  
                row.get('quantity'),
                row.get('discount'),
            )
        )

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline de ETL para CSV e PostgreSQL',
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_csv = PythonOperator(
        task_id='extract_from_csv',
        python_callable=extract_from_csv,
        provide_context=True
    )

    load_pg = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres,
        provide_context=True
    )

    extract_csv >> load_pg
