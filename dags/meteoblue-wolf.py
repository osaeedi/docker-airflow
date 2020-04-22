from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the meteoblue-wolf docker container',
    'depend_on_past': False,
    'start_date': datetime(2020, 4, 19),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('meteoblue-wolf', default_args=default_args, schedule_interval="10 * * * *", catchup=False) as dag:
    process_upload = DockerOperator(
        task_id='process-upload',
        image='meteoblue-wolf:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/meteoblue_wolf/etl.sh ',
        container_name='meteoblue-wolf',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

    ods_publish = DockerOperator(
        task_id='ods-publish',
        image='ods-publish:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m ods_publish.etl da_1wb331,da_0ok4u4',
        container_name='meteoblue-wolf--ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        retry=5,
        retry_delay=timedelta(minutes=5)
    )

    process_upload >> ods_publish
