"""
# stata_parzellen
This DAG updates the following datasets:

- [100202](https://data.bs.ch/explore/dataset/100202)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the stata_parzellen docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 9, 21),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('stata_parzellen', default_args=default_args, schedule_interval="0 2 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='stata_parzellen:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m stata_parzellen.etl',
        container_name='stata_parzellen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-DataExch/StatA/Parzellen:/code/data-processing/stata_parzellen/data_orig']
    )

