import json

import requests

##Server IP
server_ip = "81.187.83.90:5800"

##Client info inlucing version and build date
client_info = {
    "Client Version": "1.1"
}

##Applying version info to easy to use variable
client_version = client_info["Client Version"]

##Get server info through API
with requests.get(f"http://{server_ip}/version") as server_info:
    ##Make sure connection to server succeded
    if server_info.status_code == 200:
        server_version = json.loads(server_info.content)["Server Version"]
        # print(f"Server version: {server_version}\nClient version: {client_version}")

    ##If connection failed, prompt user to try again then stop program from running since it requires a server connection
    else:
        print("Server error. Please check your internet connection and try again.")
        exit(0)

##Check client version against server version and if the client is out of date prompt user to run update script
if client_version != server_version:
    print("Client out of date please update by running \"update.py\"")
    print("The program will continue to run and will probably run correctly but it is recommended that you update.")

##Main script##
identifiers = json.loads(requests.get(f"http://{server_ip}/").content)["identifiers"]
questions = json.loads(requests.get(f"http://{server_ip}/").content)["questions"]["Identifiers"]

past_questions = 0
past_questions_5 = 0
answers = []

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
                answers.append(1)
                break
            elif tempanswer == "n":
                answers.append(0)
                break
            else:
                print("Invalid input. Please try again and only use \"y\" or \"n\".")
                continue

    past_questions += 1
    past_questions_5 += 1

    if past_questions == len(identifiers):
        print("Hmm, i think im getting somewhere tell me if im right with my next guess.")
        while True:
            correct = input("Is your animal the " + str(
                json.loads(requests.post(f"http://{server_ip}/", json={"answers": answers}).content)[
                    "result"]) + "? \"y\" or \"n\"\n")
            if correct == "y":
                print("Yay thats great feel free to run me again to see if i can guess your next animal.")
                break
            elif correct == "n":
                animal_name = input("Thats too bad guess ive never seen your animal before, whats its name?\n")
                answers.insert(0, animal_name)
                requests.post(f"http://{server_ip}/update_db", json={"answers": answers})
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
            correct = input("Is your animal the " + str(
                json.loads(requests.post(f"http://{server_ip}/", json={"answers": tempanswers}).content)[
                    "result"]) + "? \"y\" or \"n\"\n")
            if correct == "y":
                print("Yay thats great feel free to run me again to see if i can guess your next animal.")
                break
            elif correct == "n":
                print("Hmm interesting im sure i was close though, let me ask a few more questions and im sure ill be "
                      "able to guess.")
                past_questions_5 = 0
                break
            else:
                print("Invalid input. Please try again and only use \"y\" or \"n\".")
                continue
        if correct == "y":
            break
