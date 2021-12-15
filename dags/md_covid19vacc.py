"""
# md_covid19vacc.py
This DAG updates the following datasets:

- [100136](https://data.bs.ch/explore/dataset/100136)
- [100147](https://data.bs.ch/explore/dataset/100147)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the bag_coronavirus.py docker container to update impftermine and impfbereitschaft',
    'depend_on_past'        : False,
    'start_date'            : datetime(2021, 12, 15),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('md_covid19vacc', default_args=default_args, schedule_interval="15 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_impftermine = DockerOperator(
        task_id='upload_impftermine',
        image='bag_coronavirus:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/bag_coronavirus/etl_impftermine.sh ',
        container_name='bag_coronavirus--upload_impftermine',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/MD-HMW:/code/data-processing/bag_coronavirus/vmdl_data']
    )

    upload_impfbereitschaft = DockerOperator(
        task_id='upload_impfbereitschaft',
        image='bag_coronavirus:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/bag_coronavirus/etl_impfbereitschaft.sh ',
        container_name='bag_coronavirus--upload_impfbereitschaft',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/MD-HMW:/code/data-processing/bag_coronavirus/vmdl_data']
    )

    ods_publish = DockerOperator(
        task_id='ods-publish',
        image='ods-publish:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m ods_publish.etl_id 100147',
        container_name='bag_coronavirus--ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        retry=2,
        retry_delay=timedelta(minutes=5)
    )

    ods_publish << upload_impfbereitschaft << upload_impftermine
