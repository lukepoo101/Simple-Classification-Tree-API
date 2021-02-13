import pickle
import sqlite3

from Train import Train

Data = sqlite3.connect("Data.db")

identifiers = []
column_names = []

for item in list(Data.execute("PRAGMA table_info(ANIMALS)")):
    identifiers.append(item[1])
    column_names.append(item[1])
identifiers.pop(0)


def get_identifiers():
    return identifiers


def get_result(user_answers):
    if len(user_answers) != len(identifiers):
        for i in range(len(identifiers) - len(user_answers)):
            user_answers.append(0)

    classifier = pickle.load(open("final_model.sav", 'rb'))

    return str(classifier.predict([user_answers])[0])


def update_database(new_animal):
    Data = sqlite3.connect("Data.db")
    for i in range(len(new_animal)):
        if type(new_animal[i]) == str:
            new_animal[i] = "\"" + new_animal[i] + "\""
    Data.execute("INSERT INTO ANIMALS (" + (", ".join(map(str, column_names))) + ") \
          VALUES (" + (", ".join(map(str, new_animal))) + ")");
    Data.commit()
    Train()
