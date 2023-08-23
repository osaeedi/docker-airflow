"""
# parlamentsdienst_grosserrat.py
This DAG updates the following datasets:

- [100307](https://data.bs.ch/explore/dataset/100307)
- [100308](https://data.bs.ch/explore/dataset/100308)
- [100309](https://data.bs.ch/explore/dataset/100309)
- [100310](https://data.bs.ch/explore/dataset/100310)
- [100311](https://data.bs.ch/explore/dataset/100311)
- [100312](https://data.bs.ch/explore/dataset/100312)
- [100313](https://data.bs.ch/explore/dataset/100313)
- [100314](https://data.bs.ch/explore/dataset/100314)
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
        'owner'                 : 'orhan.saeedi',
        'description'           : 'Run the parlamentsdienst_grosserrat docker container',
        'depend_on_past'        : False,
        'start_date'            : datetime(2023, 8, 23),
        'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "orhan.saeedi@bs.ch", "nicolas.maire@bs.ch"],
        'email_on_failure'      : True,
        'email_on_retry'        : False,
        'retries'               : 0,
        'retry_delay'           : timedelta(minutes=15)
}

with DAG('parlamentsdienst_grosserrat', default_args=default_args, schedule_interval='0 8/12 * * *', catchup=False) as dag:
        dag.doc_md = __doc__
        upload = DockerOperator(
                task_id='upload',
                image='parlamentsdienst_grosserrat:latest',
                api_version='auto',
                auto_remove=True,
                command='/bin/bash /code/data-processing/parlamentsdienst_grosserrat/etl.sh ',
                container_name='parlamentsdienst_grosserrat',
                docker_url="unix://var/run/docker.sock",
                network_mode="bridge",
                tty=True,
                volumes=['/data/dev/workspace/data-processing:/code/data-processing']
        )
