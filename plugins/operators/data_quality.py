from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 # Define your operators params
                 redshift_conn_id = "",
                 tables = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
      
        for table in self.tables:
            records = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))
            num_records = records[0][0]
            if len(records) < 1 or len(records[0]) <1:
                raise ValueError("Data quality check failed. {} return no result".format(table))
                self.log.info("Data quality check failed. {} return no result".format(table))
            elif num_records==0:
                raise ValueError("No records in {} table".format(table))
                self.log.info("No records in {} table".format(table))
            else:
                self.log.info("Data quality check on table {} pass with {} records".format(table,num_records))