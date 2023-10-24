"""
# zefix_handelsregister.py
This DAG updates the following datasets:

- [None yet](https://data.bs.ch/explore/dataset/None yet)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'orhan.saeedi',
        'description'           : 'Run the zefix-handelsregister docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2023, 10, 20),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('zefix_handelsregister', default_args=default_args, schedule_interval='0 0 * * *', catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='zefix_handelsregister:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m zefix_handelsregister.etl ',
                container_name='zefix_handelsregister',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing']
        )
