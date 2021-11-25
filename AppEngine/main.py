from flask import Flask, json
import pandas as pd
import sqlalchemy
import prop
from flask_cors import CORS
from flask_restful import Api


app = Flask(__name__)
api = Api(app)
CORS(app)

mysql_url = prop.SQL_URL
engine = sqlalchemy.create_engine(mysql_url)


@app.route('/')
def display_func():
    table = prop.TABLE
    print("Inside display_func in main.py")
    query = "Insert into " + str(table) + "(firstName, lastName) \
    values('Sambit2', 'Otta')"
    print(query)
    with engine.connect() as connection:
        result = connection.execute(query)
    print("Insert statement executed", result)
    return "SUCCESS"


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    app.run(host='127.0.0.1', port=8080, debug=True)


"""
    #df = pd.read_sql_query(query, engine)
    #dff = (df.columns.values).tolist()
    #out = df.to_json(orient='records')
    #print(out)
    #out = json.loads(str(out))
    #dict = {}
    #dict['data'] = out
    #dict['columns'] = dff
    #dict1 = json.dumps(dict)
"""
