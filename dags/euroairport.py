"""
# euroairport
This DAG updates the following datasets:

- [100078](https://data.bs.ch/explore/dataset/100078)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the euroairport docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 5, 14),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=30)
}

with DAG('euroairport', default_args=default_args, schedule_interval="0 8 * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='euroairport:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/euroairport/etl.sh ',
                container_name='euroairport',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch/EuroAirport:/code/data-processing/euroairport/data', '/data/dev/workspace/data-processing:/code/data-processing']
        )

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl_id 100078',
                container_name='euroairport--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=5,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish