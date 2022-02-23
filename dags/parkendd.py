"""
# parkendd
This DAG updates the following datasets:

- [100014](https://data.bs.ch/explore/dataset/100014)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the parkendd docker container',
    'depend_on_past': False,
    'start_date': datetime(2020, 5, 20),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('parkendd', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='parkendd:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/parkendd/etl.sh ',
        container_name='parkendd',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

    # ods_publish = DockerOperator(
    #     task_id='ods-publish',
    #     image='ods-publish:latest',
    #     api_version='auto',
    #     auto_remove=True,
    #     command='python3 -m ods_publish.etl_id 100014',
    #     container_name='parkendd--ods-publish',
    #     docker_url="unix://var/run/docker.sock",
    #     network_mode="bridge",
    #     tty=True,
    #     volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
    #     retry=5,
    #     retry_delay=timedelta(minutes=5)
    # )
    #
    # process_upload >> ods_publish
