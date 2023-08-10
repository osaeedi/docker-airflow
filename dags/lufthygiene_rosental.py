"""
# bafu_hydro_daten
This DAG updates the following dataset:

- [100275](https://data.bs.ch/explore/dataset/100275)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'hester.pieters',
        'description'           : 'Run the lufthygiene_rosental docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2023, 4, 14),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=3)
}

with DAG('lufthygiene_rosental', default_args=default_args, schedule_interval="*/30 * * * *", catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='lufthygiene_rosental:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m lufthygiene_rosental.etl',
                container_name='lufthygiene_rosental',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing']
        )
