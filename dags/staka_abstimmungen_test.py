"""
# staka_abstimmungen_test
This DAG updates the test version of the 2 datasets that cover the latest polls:

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
    'start_date': datetime(2021, 6, 1),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('staka_abstimmungen_test', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='staka_abstimmungen:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/staka_abstimmungen/etl.sh ',
        container_name='staka_abstimmungen_test',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-DataExch/StatA/Wahlen-Abstimmungen:/code/data-processing/staka_abstimmungen/data']
    )

    ods_publish = DockerOperator(
        task_id='ods-publish',
        image='ods-publish:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m ods_publish.etl_id 100141,100142',
        container_name='staka_abstimmungen_test--ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        retry=5,
        retry_delay=timedelta(minutes=5)
    )

    process_upload >> ods_publish
