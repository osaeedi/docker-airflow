from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the aue-umweltlabor docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 3, 3),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=30)
}

with DAG('aue-umweltlabor', default_args=default_args, schedule_interval="0 6 * * *", catchup=False) as dag:
        process_upload = DockerOperator(
                task_id='process-upload',
                image='aue-umweltlabor:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/aue_umweltlabor/etl.sh ',
                container_name='aue-umweltlabor',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch/Umweltlabor:/code/data-processing/aue_umweltlabor/data_orig', '/data/dev/workspace/data-processing:/code/data-processing']
        )

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl da_20e9bc,da_uxt6fk,da_q78iuw,da_reclv8',
                container_name='aue-umweltlabor--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=5,
                retry_delay=timedelta(minutes=5)
        )

        process_upload >> ods_publish