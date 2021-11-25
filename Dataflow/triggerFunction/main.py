from __future__ import absolute_import
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
import datetime
import logging
import json


def triggerFunction(request):
    try:
        logging.info("Triggering dataflow job")
        job_id, project_id = triggerDataflow()
        logging.info("dataflow job triggered")
        logging.info(job_id, project_id)
        status = {'status': "SUCCESS", 'job_id': job_id}
        status = json.dumps(status)
        return(status)
    except Exception as E:
        print(E)
        status = {'status': "FAILURE"}
        status = json.dumps(status)
        return(status)


def triggerDataflow():
    project = 'test-project-training-1234'
    template = 'gs://sam-dataflow-test/templates/dataflow-demo'
    dataflow_job = 'dataflow_demo_job' + "_" + \
                    str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
    credentials = GoogleCredentials.get_application_default()
    dataflow = googleapiclient.discovery.build('dataflow', 'v1b3', credentials=credentials)
    request = dataflow.projects().templates().launch(
        projectId=project,
        gcsPath=template,
        body={
            'jobName': dataflow_job,
            }
        )

    response = request.execute()
    print(type(response))
    job_id = response['job']['id']
    print("Printing result job id -->", job_id)
    project_id = response['job']['projectId']
    return (job_id, project_id)


if __name__ == '__main__':
    triggerFunction()
