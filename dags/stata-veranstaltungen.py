from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the stata-veranstaltungen docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 3, 3),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : True,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=30)
}

with DAG('stata-veranstaltungen', default_args=default_args, schedule_interval="0 20 * * *", catchup=False) as dag:
        t1 = DockerOperator(
                task_id='stata-veranstaltungen',
                image='stata-veranstaltungen:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/stata_veranstaltungen/etl.sh ',
                container_name='stata-veranstaltungen',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch/StatA/Veranstaltung:/code/data-processing/stata_veranstaltungen/data', '/data/dev/workspace/data-processing:/code/data-processing']
        )

        t1