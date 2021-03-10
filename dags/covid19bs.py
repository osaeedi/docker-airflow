"""
# covid19bs
This DAG updates the following datasets:

- [100073](https://data.bs.ch/explore/dataset/100073)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the covid19bs docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 6, 22),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('covid19bs', default_args=default_args, schedule_interval="*/10 * * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='covid19bs:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/covid19bs/etl.sh ',
                container_name='covid19bs',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                         '/mnt/OGD-DataExch/MD/upload:/code/data-processing/covid19bs/data_orig']
        )

        ods_publish = DockerOperator(
                task_id='ods-publish',
                image='ods-publish:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m ods_publish.etl_id 100073',
                container_name='covid19bs--ods-publish',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
                retry=2,
                retry_delay=timedelta(minutes=5)
        )

        upload >> ods_publish