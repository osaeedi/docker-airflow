from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the md_covid19cases docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 11, 17),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('md_covid19cases', default_args=default_args, schedule_interval=None, catchup=False) as dag:
        upload = DockerOperator(
                task_id='upload',
                image='md_covid19cases:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/md_covid19cases/etl.sh ',
                container_name='md_covid19cases',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/MD/upload:/code/data-processing/md_covid19cases/data_orig', '/mnt/OGD-DataExch/MD/ogd_upload:/code/data-processing/md_covid19cases/data']
        )

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl da_26x05x,da_whajy4',
                container_name='md_covid19cases--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=2,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish