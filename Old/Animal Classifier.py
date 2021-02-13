import csv
import json

import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

with open("Animals.csv", "wb") as f:
    csv_url = "http://public.terraurbs.com/Python-Projects/Animal-Classification/Animals.csv"
    r = requests.get(csv_url)
    f.write(r.content)

with open("Questions.json", "wb") as f:
    json_url = "http://public.terraurbs.com/Python-Projects/Animal-Classification/Questions.json"
    r = requests.get(json_url)
    f.write(r.content)

dataset = pd.read_csv("Animals.csv")

X = dataset.drop('Animal', axis=1)
y = dataset['Animal']
print(dataset)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

classifier = DecisionTreeClassifier()
classifier.fit(X, y)

identifiers = list(dataset.columns)
identifiers.pop(0)
print(identifiers)

past_questions = 0
past_questions_5 = 0
answers = []
questions = json.load(open("Questions.json", "r"))["Identifiers"]

for question_number in identifiers:

    if questions[question_number]["type"] == "int":
        while True:
            try:
                tempanswer = int(input(questions[question_number]["question"] + "\n"))
                break
            except:
                print("Invalid input. Please try again and only use whole numbers.")
                continue

        answers.append(tempanswer)

    else:
        while True:
            tempanswer = input(questions[question_number]["question"] + " \"y\" or \"n\"\n")
            if tempanswer == "y":
                answers.append(True)
                break
            elif tempanswer == "n":
                answers.append(False)
                break
            else:
                print("Invalid input. Please try again and only use \"y\" or \"n\".")
                continue

    past_questions += 1
    past_questions_5 += 1

    if past_questions == len(identifiers):
        print("Hmm, i think im getting somewhere tell me if im right with my next guess.")
        while True:
            correct = input("Is your animal the " + str(classifier.predict([answers])[0]) + "? \"y\" or \"n\"\n")
            if correct == "y":
                print("Yay thats great feel free to run me again to see if i cna guess your next animal.")
                break
            elif correct == "n":
                animal_name = input("Thats too bad guess ive never seen your animal before, whats its name?\n")
                answers.insert(0, animal_name)
                with open("Animals.csv", "a") as f:
                    wr = csv.writer(f)
                    wr.writerow(answers)
                break
            else:
                print("Invalid input. Please try again and only use \"y\" or \"n\".")
                continue
        if correct == "y":
            break

    elif past_questions_5 == 5:
        tempanswers = list(answers)
        for i in range(len(identifiers) - len(answers)):
            tempanswers.append(0)
        print("Hmm, i think im getting somewhere tell me if im right with my next guess.")
        while True:
            correct = input("Is your animal the " + str(classifier.predict([tempanswers])[0]) + "? \"y\" or \"n\"\n")
            if correct == "y":
                print("Yay thats great feel free to run me again to see if i cna guess your next animal.")
                break
            elif correct == "n":
                print("Hmm interesting im sure i was close though let me ask a few more questions and im sure ill be "
                      "able to guess.")
                past_questions_5 = 0
                break
            else:
                print("Invalid input. Please try again and only use \"y\" or \"n\".")
                continue
        if correct == "y":
            break
