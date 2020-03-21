import database
import os
import pandas as pd

# Replace with download scripts
DIR = os.path.abspath(os.path.dirname(__file__))
train = pd.read_csv(os.path.join(DIR, '../data/raw/train.csv'))
test = pd.read_csv(os.path.join(DIR, '../data/raw/test.csv'))

# Save data to database
uri, db, _ = database.get_config()
database.save(train, uri, db, 'dev', 'raw_train')
database.save(test, uri, db, 'dev', 'raw_test')
