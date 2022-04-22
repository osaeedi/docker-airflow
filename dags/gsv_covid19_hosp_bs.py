"""
# gsv_covid19_hosp_bs.py
This DAG helps populating the following datasets:

- [100109](https://data.bs.ch/explore/dataset/100109)

"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the gsv_covid19_hosp_bs.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2021, 12, 17),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('gsv_covid19_hosp_auto', default_args=default_args, schedule_interval='*/2 7-21 * * *', catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='gsv_covid19_hosp_bs:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/gsv_covid19_hosp_bs/etl.sh ',
        container_name='gsv_covid19_hosp_bs--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
