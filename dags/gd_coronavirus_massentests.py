"""
# gd_coronavirus_massentests
This DAG updates the following datasets:

- [100145](https://data.bs.ch/explore/dataset/100145)
- [100146](https://data.bs.ch/explore/dataset/100146)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the gd_coronavirus_massentests docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2021, 6, 7),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('gd_coronavirus_massentests', default_args=default_args, schedule_interval="None", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='gd_coronavirus_massentests:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/gd_coronavirus_massentests/etl.sh ',
        container_name='gd_coronavirus_massentests--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/GD-GS/coronavirus-massentests:/code/data-processing/gd_coronavirus_massentests/data']
    )

    ods_publish = DockerOperator(
        task_id='ods-publish',
        image='ods-publish:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m ods_publish.etl_id 9999', #100145,100146',
        container_name='gd_coronavirus_massentests--ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        retry=2,
        retry_delay=timedelta(minutes=5)
    )

    upload >> ods_publish
