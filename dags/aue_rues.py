"""
# aue_rues
This DAG updates the following datasets:

- [100046](https://data.bs.ch/explore/dataset/100046)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the aue_rues docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 1, 5),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('aue_rues', default_args=default_args, schedule_interval="*/10 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='aue_rues:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m aue_rues.etl',
        container_name='aue_rues--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

