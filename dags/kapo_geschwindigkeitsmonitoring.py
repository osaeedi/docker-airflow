"""
# kapo_geschwindigkeitsmonitoring
This DAG updates the following datasets:

- [100112](https://data.bs.ch/explore/dataset/100112)
- [100115](https://data.bs.ch/explore/dataset/100115)
- [100097](https://data.bs.ch/explore/dataset/100097)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the kapo_geschwindigkeitsmonitoring docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2021, 1, 20),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('kapo_geschwindigkeitsmonitoring', default_args=default_args, schedule_interval='0 2 * * *', catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='kapo_geschwindigkeitsmonitoring:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/kapo_geschwindigkeitsmonitoring/etl.sh ',
                container_name='kapo_geschwindigkeitsmonitoring',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch/KaPo/VP-Geschwindigkeitsmonitoring:/code/data-processing/kapo_geschwindigkeitsmonitoring/data_orig',
                         '/data/dev/workspace/data-processing:/code/data-processing']
        )
        #
        # ods_publish = DockerOperator(
        #         task_id='ods-publish',
        #         image='ods-publish:latest',
        #         api_version='auto',
        #         auto_remove=True,
        #         command='python3 -m ods_publish.etl_id 100112,100115,100097',
        #         container_name='kapo_geschwindigkeitsmonitoring--ods-publish',
        #         docker_url="unix://var/run/docker.sock",
        #         network_mode="bridge",
        #         tty=True,
        #         volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        #         retry=2,
        #         retry_delay=timedelta(minutes=5)
        # )
        #
        # upload >> ods_publish