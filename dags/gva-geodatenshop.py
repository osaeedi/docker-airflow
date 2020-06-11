from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the gva-geodatenshop docker container',
    'depend_on_past': False,
    'start_date': datetime(2020, 6, 11),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('gva-geodatenshop', default_args=default_args, schedule_interval="0 5 * * *", catchup=False) as dag:
    process_upload = DockerOperator(
        task_id='process-upload',
        image='gva-geodatenshop:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/gva_geodatenshop/etl.sh ',
        container_name='gva-geodatenshop',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-GVA:/code/data-processing/gva_geodatenshop/data_orig']
    )

# todo: run harvester

process_upload
