from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the verkehrszaehldaten docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 6, 4),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('verkehrszaehldaten', default_args=default_args, schedule_interval="0 4 * * *", catchup=False) as dag:
        upload = DockerOperator(
                task_id='upload',
                image='verkehrszaehldaten:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/verkehrszaehldaten/etl.sh ',
                container_name='verkehrszaehldaten',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                         '/mnt/MOB-StatA:/code/data-processing/verkehrszaehldaten/data_orig']
        )

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl da_koisz3 da_ob8g0d',
                container_name='verkehrszaehldaten--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=5,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish