"""
# smarte_strasse_schallsensor
This DAG updates the following datasets:

- [100170](https://data.bs.ch/explore/dataset/100170)
- [100172](https://data.bs.ch/explore/dataset/100172)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the smarte_strasse_schall docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2022, 1, 20),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('smarte_strasse_schallsensor', default_args=default_args, schedule_interval="*/5 * * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='smarte_strasse_schall:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/smarte_strasse_schall/etl.sh ',
                container_name='smarte_strasse_schall',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing']
        )
