from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'airflow',
        'description'           : 'Run the aue-umweltlabor container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2020, 3, 3),
        'email'                 : ["opendata@bs.ch"],
        'email_on_failure'      : False,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=30)
}

with DAG('aue-umweltlabor', default_args=default_args, schedule_interval="0 6 * * *", catchup=False) as dag:
        t1 = DockerOperator(
                task_id='aue-umweltlabor',
                image='aue-umweltlabor:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/aue_umweltlabor/etl.sh ',
                container_name='aue-umweltlabor',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge", 
                tty=True,
                volumes=['/mnt/OGD-DataExch/Umweltlabor:/code/data-processing/aue_umweltlabor/data_orig', '/data/dev/workspace/data-processing:/code/data-processing']
        )

        t1