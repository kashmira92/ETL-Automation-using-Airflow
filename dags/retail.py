from airflow.decorators import dag, task
from datetime import datetime

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator

from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType
import pandas as pd
from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig

@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail'],
)
def retail():

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='include/dataset/online_retail.csv',
        dst='raw/online_retail.csv',
        bucket='kash_online_retail_bucket',
        gcp_conn_id='gcp',
        mime_type='text/csv',
        # encoding='utf-8',
    )

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='gcp',
    )

    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://kash_online_retail_bucket/raw/online_retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
            # encoding='utf-8',
        ),
        output_table=Table(
            name='raw_invoices1',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )

    # @task
    # def gcs_to_raw():
    #     # Load CSV file to pandas DataFrame with specified encoding
    #     df = pd.read_csv(
    #         'gs://kash_online_retail_bucket/raw/online_retail.csv',
    #         encoding='utf-8',  # Add encoding parameter here
    #     )

    #     # Further processing or loading to BigQuery can be done here
    #     # For example, if you want to load to BigQuery using pandas:
    #     df.to_gbq(destination_table='ETL-Automation-Airflow-pn.retail.retail_invoices1',
    #              project_id='etl-automation-airflow-pn', if_exists='replace')

    # upload_csv_to_gcs >> create_retail_dataset >> gcs_to_raw

@task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    check_load()

    transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']))
    
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    check_transform()

    report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        )
    )
    
retail()

    
