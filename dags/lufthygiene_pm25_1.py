"""
# lufthygiene_pm25
This DAG updates the following datasets:

- [100081](https://data.bs.ch/explore/dataset/100081)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the lufthygiene_pm25 docker container',
    'depend_on_past': False,
    'start_date': datetime(2021, 2, 22),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('lufthygiene_pm25_1', default_args=default_args, schedule_interval="*/15 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='lufthygiene_pm25:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m lufthygiene_pm25.etl',
        container_name='lufthygiene_pm25',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
