"""
# covid19dashboard
This DAG updates the following datasets:

- [100085](https://data.bs.ch/explore/dataset/100085)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the covid19dashboard docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 5, 18),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('covid19dashboard', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='covid19dashboard:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/covid19dashboard/etl.sh ',
                container_name='covid19dashboard',
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
                command='python3 -m ods_publish.etl_id 100085',
                container_name='covid19dashboard--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=5,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish