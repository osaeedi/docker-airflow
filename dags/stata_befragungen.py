"""
# stata_befragungen
This DAG updates the datasets outlined [here](https://data.bs.ch/explore/?sort=modified&q=befragung+statistisches+amt).
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the stata_befragungen docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 8, 29),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('stata_befragungen', default_args=default_args, schedule_interval="5,35 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='stata_befragungen:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m stata_befragungen.etl',
        container_name='stata_befragungen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-DataExch/StatA/Befragungen:/code/data-processing/stata_befragungen/data_orig']
    )

