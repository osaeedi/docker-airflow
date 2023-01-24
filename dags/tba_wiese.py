"""
# tba_wiese
This DAG updates the following datasets:

- [100269](https://data.bs.ch/explore/dataset/100269)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the tba_wiese docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 1, 24),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('tba_wiese', default_args=default_args, schedule_interval="30 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='tba_wiese:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m tba_wiese.etl',
        container_name='tba_wiese--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

