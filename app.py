from flask import Flask
from flask_restful import Api
from routes import register_routes

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

api = Api(app)



if __name__ == '__main__':
    register_routes(api=api)
    app.run(port=9833, debug=True, host='0.0.0.0')