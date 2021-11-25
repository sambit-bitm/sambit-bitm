from google.cloud import storage
import time
import logging


def gcs_generic(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    from google.cloud import error_reporting
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('File: {}'.format(data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))
    logging.info("Inside logging")
    client = error_reporting.Client()
    client.report("An error has occurred.")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    bucket_name = data['bucket']
    blob_name = data['name']
    destination_bucket_name = 'sam-demo-18052020_backup'
    destination_blob_name = data['name'] + "_" + timestr

    copy_blob(bucket_name, blob_name, destination_bucket_name,
              destination_blob_name)


def copy_blob(
        bucket_name, blob_name, destination_bucket_name, destination_blob_name
            ):
    """Copies a blob from one bucket to another with a new name."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    # destination_bucket_name = "destination-bucket-name"
    # destination_blob_name = "destination-object-name"

    storage_client = storage.Client()
    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )
    print("Back up created ")
