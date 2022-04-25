"""
# parlamentsdienst_gr_abstimmungen
This DAG updates the following datasets:

- [100186](https://data.bs.ch/explore/dataset/100186)
- [100188](https://data.bs.ch/explore/dataset/100188)
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'jonas.bieri',
    'description'           : 'Run the parlamentsdienst_gr_abstimmungen docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 3, 29),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('parlamentsdienst_gr_abstimmungen', default_args=default_args, schedule_interval="*/2 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload_bag_datasets = DockerOperator(
        task_id='upload',
        image='parlamentsdienst_gr_abstimmungen:latest',
        api_version='auto',
        auto_remove=True,
        command='python3 -m parlamentsdienst_gr_abstimmungen.etl',
        container_name='parlamentsdienst_gr_abstimmungen--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing']
    )

