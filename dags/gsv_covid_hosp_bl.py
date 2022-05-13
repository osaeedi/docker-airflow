from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the gsv_covid19_hosp_bl.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 5, 13),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('gsv_covid19_hosp_bl', default_args=default_args, schedule_interval='*/2 7-22 * * *', catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='gsv_covid19_hosp_bl:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/gsv_covid19_hosp_bl/etl.sh ',
        container_name='gsv_covid19_hosp_bl--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
