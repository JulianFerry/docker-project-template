import os
import pandas as pd
import joblib

from flask import Flask, request
from flask_restful import Api, Resource

DIR = os.path.abspath(os.path.dirname(__file__))


# Start RESTful app
app = Flask(__name__)
api = Api(app)


def load_pickle():
    app.config['preprocessor'] = joblib.load(os.environ['preprocessor_path'])
    app.config['model'] = joblib.load(os.environ['model_path'])


class Predict(Resource):
    """
    Return trained model predictions (data is transformed first)

    The POST request needs to contain a 'data' argument, as either:
    - CSV file
    - JSON string

    Example
    -------
    ``curl -X POST -F data=@data/raw/test.csv http://127.0.0.1:8080/``

    """

    def get(self):
        response = {
            'status': 'success',
            'message': 'Flask app is up and running'}
        return response, 200

    def post(self):
        """
        Handles post request

        """
        # Load data
        if request.json and 'data' in request.json.keys():
            print('JSON data received. Scoring data...')
            X = pd.DataFrame(request.json['data'])
        elif request.files and 'data' in request.files.keys():
            print('File received. Scoring data...')
            X = pd.read_csv(request.files['data'])
        # Check that data has been sent as a file or as json
        elif not (request.files or request.json):
            response = {
                'status': 'error',
                'message': 'Send data as file or json in a POST request'
            }
            return response, 400

        # Preprocess data and make predictions
        if not app.config.get('model') or not app.config.get('preprocessor'):
            load_pickle()
        X_pp = app.config['preprocessor'].transform(X)
        y_pred = app.config['model'].predict(X_pp)
        # Respond with predictions
        print('Successfully scored data using model.')
        response = {
            'status': 'success',
            'data': list(y_pred)
        }
        return response, 200


# Add endpoints to RESTful api
api.add_resource(Predict, '/')


# For local debugging only
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
