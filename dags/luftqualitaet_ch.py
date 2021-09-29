"""
# luftqualitaet_ch
This DAG updates the following datasets:

- [100048](https://data.bs.ch/explore/dataset/100048)
- [100049](https://data.bs.ch/explore/dataset/100049)
- [100050](https://data.bs.ch/explore/dataset/100050)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the luftqualitaet_ch docker container',
    'depend_on_past': False,
    'start_date': datetime(2021, 9, 29),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('luftqualitaet_ch', default_args=default_args, schedule_interval="15 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='luftqualitaet_ch:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/luftqualitaet_ch/etl.sh ',
        container_name='luftqualitaet_ch',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
