"""
# itbs_klv
This DAG updates the following datasets:

- [100324](https://data.bs.ch/explore/dataset/100324)
- [100325](https://data.bs.ch/explore/dataset/100325)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'orhan.saeedi',
    'description'           : 'Run the itbs_klv docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2023, 11, 7),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('itbs_klv', default_args=default_args, schedule_interval="*/2 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='itbs_klv:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m itbs_klv.etl',
        container_name='itbs_klv--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )
