from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_restful import Api
from routes import register_routes
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)



if __name__ == '__main__':

    from config.pinecone_service.pc_config import ensure_pinecone_index
    ensure_pinecone_index()

    register_routes(api = api)

    app.run(port = 9833, debug = True, host = '0.0.0.0')