 Create a template
 python dataflow-demo.py \
    --runner  DataFlowRunner \
    --project test-project-training-1234 \
    --staging_location gs://sam-dataflow-test/staging \
    --temp_location gs://sam-dataflow-test/temp \
    --template_location gs://sam-dataflow-test/templates/dataflow-demo\
    --machine_type n1-standard-4\
    --region asia-south1\
    --worker_region asia-south1\
    --job_name dataflow-demo\
    --requirements_file requirements.txt

Run locally
 python dataflow-demo.py \
    --runner  DataFlowRunner \
    --project test-project-training-1234 \
    --staging_location gs://sam-dataflow-test/staging \
    --temp_location gs://sam-dataflow-test/temp \
    --machine_type n1-standard-4\
    --region us-central1\
    --worker_region us-central1\
    --job_name dataflow-demo