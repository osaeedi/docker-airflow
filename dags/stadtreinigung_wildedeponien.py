"""
# stadtreinigung_wildedeponien
This DAG updates the following datasets:

- [100070](https://data.bs.ch/explore/dataset/100070)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the stadtreinigung_wildedeponien docker container',
    'depend_on_past': False,
    'start_date': datetime(2023, 2, 14),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=3)
}

with DAG('stadtreinigung_wildedeponien', default_args=default_args, schedule_interval="0 7,14 * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    process_upload = DockerOperator(
        task_id='process-upload',
        image='stadtreinigung_wildedeponien:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m stadtreinigung_wildedeponien.etl',
        container_name='stadtreinigung_wildedeponien--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

