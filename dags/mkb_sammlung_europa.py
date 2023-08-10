"""
# mkb_sammlung_europa.py
This DAG updates the following datasets:

- [100148](https://data.bs.ch/explore/dataset/100148)

"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the mkb_sammlung_europa.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 1, 27),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('mkb_sammlung_europa', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='mkb_sammlung_europa:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/mkb_sammlung_europa/etl.sh ',
        container_name='mkb_sammlung_europa--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/PD-Kultur-MKB:/code/data-processing/mkb_sammlung_europa/data']
    )