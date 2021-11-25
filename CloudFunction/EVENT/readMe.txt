gcloud functions deploy hello_gcs_generic --service-account gcp-training-sa-1@test-project-training-1234.iam.gserviceaccount.com \
	--runtime python37 --trigger-resource sam-demo-18052020 \
	--trigger-event google.storage.object.finalize --timeout=540s 