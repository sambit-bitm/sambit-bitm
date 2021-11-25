from __future__ import absolute_import
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, \
                GoogleCloudOptions, StandardOptions, SetupOptions, WorkerOptions
import logging
from apache_beam.options.value_provider import StaticValueProvider
import prop


options = PipelineOptions()
# google_cloud_options = options.view_as(GoogleCloudOptions)
# google_cloud_options.project = 'test-project-training-1234'
# google_cloud_options.job_name = 'dataflow-demo-test'
# google_cloud_options.staging_location = 'gs://sam-dataflow-test/staging_file'
# google_cloud_options.temp_location = 'gs://sam-dataflow-test/temp_file'
# google_cloud_options.region = 'asia-south1'
# options.view_as(StandardOptions).runner = 'DataflowRunner'
# options.view_as(WorkerOptions).machine_type = 'n1-standard-4'
# options.view_as(SetupOptions).save_main_session = True

# table_schema = 'EmpId:INTEGER, FirstName:STRING,  LastName:STRING, Age:INTEGER'
table_schema = prop.TABLE_SCHEMA


class addAgeDoFn(beam.DoFn):
    def __init__(self):
        logging.info("Going to add age")

    def process(self, element):
        logging.info("Going to add age method")
        row = element
        row['Age'] = int(row['Age']) + 5
        yield row


def run(argv=None):
    try:
        # tablespec = 'test-project-training-1234:mytest.society'
        tablespec = prop.TABLE

        with beam.Pipeline(options=options) as p:
            rawData = p | 'ReadData' >> beam.io.ReadFromText(prop.INPUT_FILE,
                                                             skip_header_lines=1) \
                    | 'Split' >> beam.Map(lambda x: x.split(',')) \
                    | 'format to dict' >> beam.Map(lambda x: {"EmpId": x[0],
                                                              "FirstName": x[1],
                                                              "LastName": x[2],
                                                              "Age": x[3]}) \
                    | 'Add to age' >> beam.ParDo(addAgeDoFn())
            rawData | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                tablespec,
                schema=table_schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )

    except Exception as e:
        errormsg = {"message": "Error Occured "+str(e)}
        print(errormsg)


if __name__ == '__main__':
    run()
