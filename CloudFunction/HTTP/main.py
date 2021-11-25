import prop
import pandas as pd
import sqlalchemy
import datetime as datetime
from google.cloud import storage


mysql_url = prop.SQL_URL
engine = sqlalchemy.create_engine(mysql_url)


def signed_url(bucket_name, blob_name):
    try:
        print("Bucket-->", bucket_name)
        print("blob_name-->", blob_name)
        storage_client = storage.Client.from_service_account_json(
                        'gcs_admin_key.json'
                        )
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        url = blob.generate_signed_url(
                                    expiration=datetime.timedelta(minutes=2),
                                    method='GET')
        print('Completed generation of signed URL')
        # print("Printing signed URL-->, 'curl \'{}\''.format(url))
        print('\'{}\''.format(url))
        return(url)
    except Exception as e:
        print("error -->", str(e))


def insert_func(request):
    try:
        table = prop.TABLE
        print("Inside display_func in main.py")
        query = "Select * from  " + str(table)
        print(query)
        df = pd.read_sql_query(query, engine)
        # columns = (df.columns.values).tolist()
        # column_values = df.to_json(orient='records')
        # final_output = json.loads(str(column_values))
        # result = {}
        # result['data'] = final_output
        # result['columns'] = columns
        # final_result = json.dumps(result)
        bucket_name = prop.BUCKET_NAME
        bucket_path = 'gs://' + bucket_name
        object_name = bucket_path + '/' + prop.FILENAME
        print("The file name is  --> ", object_name)
        df.to_csv(object_name, sep=',', encoding='utf-8', index=False)
        print("Sent to GCS")
        # gcs_url = 'https://storage.googleapis.com/' + bucket_name + '/' + prop.FILENAME
        new_signed_url = signed_url(bucket_name, prop.FILENAME)
        return new_signed_url
    except Exception as e:
        print("error -->", str(e))


if __name__ == '__main__':
    insert_func()
