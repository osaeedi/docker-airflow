"""
# aue_grundwasser
This DAG updates the following datasets:

- [100164](https://data.bs.ch/explore/dataset/100164)
- [100179](https://data.bs.ch/explore/dataset/100179)
- [100180](https://data.bs.ch/explore/dataset/100180)
- [100181](https://data.bs.ch/explore/dataset/100181)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the aue_grundwasser docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 2, 23),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('aue_grundwasser', default_args=default_args, schedule_interval="25 5 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='aue_grundwasser:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m aue_grundwasser.etl',
        container_name='aue_grundwasser--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

