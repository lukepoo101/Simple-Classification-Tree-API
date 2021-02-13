import pickle
import sqlite3

import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def Train():
    print("Training")
    Database_Connection = sqlite3.connect("Data.db")

    query = "SELECT * from ANIMALS"

    dataset = pd.read_sql_query(query, Database_Connection)

    X = dataset.drop('name', axis=1)
    y = dataset['name']

    model = DecisionTreeClassifier()
    model.fit(X, y)

    savename = "final_model.sav"
    pickle.dump(model, open(savename, "wb"))
