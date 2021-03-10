"""
# stata_veranstaltungen
This DAG updates the 2 datasets that cover the latest polls. At time of this writing, these are:

- [100074](https://data.bs.ch/explore/dataset/100074)
"""
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
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=30)
}

with DAG('stata_veranstaltungen', default_args=default_args, schedule_interval="0 20 * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
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

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl_id 100074',
                container_name='stata-veranstaltungen--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=5,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish