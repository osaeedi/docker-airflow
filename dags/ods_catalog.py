"""
# ods_catalog
This DAG updates the following datasets:

- [100057](https://data.bs.ch/explore/dataset/100057)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the ods_catalog docker container',
    'depend_on_past': False,
    'start_date': datetime(2021, 2, 4),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}


with DAG('ods_catalog', default_args=default_args, schedule_interval='3 * * * *', catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='ods_catalog:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m ods_catalog.etl',
        container_name='ods_catalog',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
