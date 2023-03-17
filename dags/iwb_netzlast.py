"""
# iwb_netzlast.py
This DAG updates the following datasets:

- [100233](https://data.bs.ch/explore/dataset/100233)

"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner'                 : 'hester.pieters',
    'description'           : 'Run the iwb_netzlast.py docker container',
    'depend_on_past'        : False,
    'start_date'            : datetime(2022, 6, 12),
    'email'                 : ["jonas.bieri@bs.ch", "jonas.eckenfels@bs.ch", "hester.pieters@bs.ch"],
    'email_on_failure'      : True,
    'email_on_retry'        : False,
    'retries'               : 0,
    'retry_delay'           : timedelta(minutes=15)
}

with DAG('iwb_netzlast', default_args=default_args, schedule_interval="0 * * * *", catchup=False) as dag:
    dag.doc_md = __doc__
    upload = DockerOperator(
        task_id='upload',
        image='iwb_netzlast:latest',
        api_version='auto',
        auto_remove=True,
        command='/bin/bash /code/data-processing/iwb_netzlast/etl.sh ',
        container_name='iwb_netzlast--upload',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        tty=True,
        volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/IWB/Netzlast:/code/data-processing/iwb_netzlast/data']
    )

    # fit_model = DockerOperator(
    #     task_id='fit_model',
    #     image='stromverbrauch:latest',
    #     api_version='auto',
    #     auto_remove=True,
    #     command='Rscript /code/data-processing/stata_erwarteter_stromverbrauch/Stromverbrauch_OGD.R',
    #     container_name='stromverbrauch--fit_model',
    #     docker_url="unix://var/run/docker.sock",
    #     network_mode="bridge",
    #     tty=True,
    #     volumes=['/data/dev/workspace/data-processing:/code/data-processing', '/mnt/OGD-DataExch/StatA/Stromverbrauch:/code/data-processing/stata_erwarteter_stromverbrauch/data/export']
    # )
    #
    # upload >> fit_model
