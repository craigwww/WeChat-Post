from flask import Flask
from eve import Eve

# SETTINGS = {
#     'DOMAIN': DOMAIN,
# }

#app = Flask(__name__)
# app = Eve(settings=SETTINGS, validator=ValidatorSQL, data=SQL)
app = Eve()

# @app.route("/")
# def hello():
#     return "Hello World!"

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.myFirstMD
    return db


if __name__ == '__main__':
    app.run()

