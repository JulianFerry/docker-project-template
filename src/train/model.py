import database as db
import os
import joblib

# Define model to train here
model = None

if __name__ == "__main__":

    # Load data
    db_config = db.get_config()
    train_pp = db.load(*db_config, 'processed_train')
    X_train_pp = train_pp.drop('SalePrice', axis=1)
    y_train = train_pp['SalePrice']

    # Fit model
    model.fit(X_train_pp, y_train)

    # Save model
    DIR = os.path.abspath(os.path.dirname(__file__))
    joblib.dump(model, os.path.join(DIR, '../pickle/Model.pkl'))
