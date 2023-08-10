"""
# gd_coronavirus_abwassermonitoring.py
This DAG updates the following datasets:

- [100167](https://data.bs.ch/explore/dataset/100167)

"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the gd_coronavirus_abwassermonitoring.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 1, 21),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('gd_coronavirus_abwassermonitoring', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='gd_coronavirus_abwassermonitoring:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/gd_coronavirus_abwassermonitoring/etl.sh ',
        container_name='gd_coronavirus_abwassermonitoring--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/GD-Kantonslabor/Covid-19_Abwasser:/code/data-processing/gd_coronavirus_abwassermonitoring/data']
    )
