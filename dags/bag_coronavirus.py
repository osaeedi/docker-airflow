"""
# bag_coronavirus
This DAG updates the following datasets:

- [100094](https://data.bs.ch/explore/dataset/100094)
- [100111](https://data.bs.ch/explore/dataset/100111)
- [100116](https://data.bs.ch/explore/dataset/100116)
- [100119](https://data.bs.ch/explore/dataset/100119)
- [100123](https://data.bs.ch/explore/dataset/100123)
- [100135](https://data.bs.ch/explore/dataset/100135)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the bag_coronavirus docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2020, 8, 27),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('bag_coronavirus', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='bag_coronavirus:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/bag_coronavirus/etl_bag_datasets.sh ',
        container_name='bag_coronavirus--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/StatA/BAG_Coronavirus_Tests:/code/data-processing/bag_coronavirus/data']
    )

    upload_vmdl = DockerOperator(
        task_id='upload_vmdl',
        image='bag_coronavirus:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/bag_coronavirus/etl_vmdl.sh ',
        container_name='bag_coronavirus--upload_vmdl',
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
        command='python3 -m ods_publish.etl_id 100094,100111,100116,100119,100123,100135',
        container_name='bag_coronavirus--ods-publish',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing'],
        retry=2,
        retry_delay=timedelta(minutes=5)
    )

    ods_publish << [upload, upload_vmdl]