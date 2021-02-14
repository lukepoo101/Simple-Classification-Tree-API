import json

from Main import get_result, get_identifiers, update_database
from flask import Flask
from flask_restful import Api, Resource, reqparse

#define
app = Flask(__name__)
api = Api(app)


class AI(Resource):
    def get(self):
        return (
            {
                "identifiers": get_identifiers(),
                "questions": json.loads(open("Questions.json").read())
            }
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("answers", action='append')
        params = parser.parse_args()
        return ({
            "result": get_result(params["answers"])
        })


class Update_db(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("answers", action='append')
        params = parser.parse_args()
        update_database(params["answers"])


class Info(Resource):
    def get(self):
        try:
            with open("Server_Info.json", "r") as info:
                return (json.loads(info.read()))
        except:
            return ("Server Info not found")


class Update(Resource):
    def get(self):
        with open("Client.py", "r") as update:
            return ({
                "update": update.read()
            })


api.add_resource(AI, "/")
api.add_resource(Info, "/version", "/version/")
api.add_resource(Update, "/update", "/update/")
api.add_resource(Update_db, "/update_db", "/update_db/")

print(get_result([4, 0, 1, 1, 0]))

if __name__ == '__main__':
    app.run(debug=True, port=5800)
