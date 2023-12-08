"""
# mobilitaet_parkflaechen.py
This DAG updates the following datasets:

- [100329](https://data.bs.ch/explore/dataset/100329)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'orhan.saeedi',
        'description'           : 'Run the mobilitaet-parkflaechen docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2023, 12, 8),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('mobilitaet_parkflaechen', default_args=default_args, schedule_interval='0 0 * * *', catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='mobilitaet_parkflaechen:latest',
                api_version='auto',
                auto_remove=True,
                command='python3 -m mobilitaet_parkflaechen.etl ',
                container_name='mobilitaet_parkflaechen',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing',
                         '/mnt/OGD-DataExch/BVD-mobilitaet/Parkplatzkataster/Shape:/code/data-processing/mobilitaet_parkflaechen/data_orig']
        )
