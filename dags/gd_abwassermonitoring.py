"""
# gd_abwassermonitoring.py
This DAG updates the following datasets:

- [100302](https://data.bs.ch/explore/dataset/100302)

"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the gd_abwassermonitoring.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 6, 20),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('gd_abwassermonitoring', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='gd_abwassermonitoring:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/gd_abwassermonitoring/etl.sh ',
        container_name='gd_abwassermonitoring--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/GD-Kantonslabor/Influenza_RSV_Abwasser:/code/data-processing/gd_abwassermonitoring/data']
    )