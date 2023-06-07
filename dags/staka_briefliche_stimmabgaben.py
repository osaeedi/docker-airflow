"""
# staka_briefliche_stimmabgaben_1.py
This DAG helps populating the following datasets:

- [100223](https://data.bs.ch/explore/dataset/100223)
- [100224](https://data.bs.ch/explore/dataset/100224)

"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the staka_briefliche_stimmabgaben.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 9, 6),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=3)
}

with DAG('staka_briefliche_stimmabgaben_3', default_args=default_args, schedule_interval='*/2 * * * *', catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='staka_briefliche_stimmabgaben:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/staka_briefliche_stimmabgaben/etl.sh ',
        container_name='staka_briefliche_stimmabgaben--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-DataExch/staka-abstimmungen:/code/data-processing/staka_briefliche_stimmabgaben/data']
    )
