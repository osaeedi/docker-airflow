"""
# kapo_ordnungsbussen
This DAG updates the following datasets:

- [100058](https://data.bs.ch/explore/dataset/100058)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'jonas.bieri',
    'description': 'Run the kapo_ordnungsbussen docker container',
    'depend_on_past': False,
    'start_date': datetime(2021, 10, 7),
    'email': ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch"],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=15)
}

with DAG('kapo_ordnungsbussen', default_args=default_args, schedule_interval=None, catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='kapo_ordnungsbussen:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/kapo_ordnungsbussen/etl.sh ',
        container_name='kapo_ordnungsbussen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                 '/mnt/OGD-DataExch/KaPo/Ordnungsbussen:/code/data-processing/kapo_ordnungsbussen/data_orig'
                 ]
    )
