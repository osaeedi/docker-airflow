"""
# aue_schall
This DAG updates the following datasets:

- [100087](https://data.bs.ch/explore/dataset/100087)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'jonas.bieri',
        'description'           : 'Run the aue-schall docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 6, 24),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('aue-schall', default_args=default_args, schedule_interval="*/15 * * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='aue_schall:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/aue_schall/etl.sh ',
                container_name='aue-schall',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing']
        )

        # ods_publish = DockerOperator(
        #         task_id='ods-publish',
        #         image='ods-publish:latest',
        #         api_version='auto',
        #         auto_remove=True,
        #         #command='python3 -m ods_publish.etl da_jljxu2,da_nr71j8',
        #         command='python3 -m ods_publish.etl_id 100090',
        #         container_name='aue_schall--ods-publish',
        #         docker_url="unix://var/run/docker.sock",
        #         network_mode="bridge",
        #         tty=True,
        #         volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        #         retry=2,
        #         retry_delay=timedelta(minutes=5)
        # )
        #
        # upload >> ods_publish