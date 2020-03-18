from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "jonas.bieri",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["jonas.bieri@bs.ch"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


def throw_error(**context):
    raise ValueError('Intentionally throwing an error to send an email.')

with DAG("email-test", default_args=default_args, schedule_interval=None) as dag:   
  t1 = PythonOperator(task_id='throw_error_and_email',
                      python_callable=throw_error,
                      provide_context=True,
                      email_on_failure=True,
                      email='jonas.bieri@bs.ch',
                      dag=dag)
                      
  t1