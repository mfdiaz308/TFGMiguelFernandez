import json
from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hiWorld():
    return 'Hi World\n'

if __name__ == '__main__':
    app.run(debug=True)
