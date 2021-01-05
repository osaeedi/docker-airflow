from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the bafu_hydrodaten docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 6, 25),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('bafu_hydrodaten', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
        upload = DockerOperator(
                task_id='upload',
                image='bafu_hydrodaten:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/bafu_hydrodaten/etl.sh ',
                container_name='bafu_hydrodaten',
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
                command='python3 -m ods_publish.etl da_uuvdoh',
                container_name='bafu_hydrodaten--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=1,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish