"""
# staka_abstimmungen
This DAG updates the test and live version of the 2 datasets that cover the latest polls:

- [100141](https://data.bs.ch/explore/dataset/100141)
- [100142](https://data.bs.ch/explore/dataset/100142)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the staka_abstimmungen docker container',
    'depend_on_past': False,
    'start_date': datetime(2022, 2, 8),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('staka_abstimmungen_2', default_args=default_args, schedule_interval="*/2 9-19 * * 7", catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='staka_abstimmungen:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/staka_abstimmungen/etl_auto.sh ',
        container_name='staka_abstimmungen',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-DataExch/StatA/Wahlen-Abstimmungen:/code/data-processing/staka_abstimmungen/data']
    )
