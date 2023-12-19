import json
from flask import Flask, render_template, request
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search']
        print("Search query:", search_query)
        # Redirects back to the home page for now
        return render_template('index.html')
    # If it's a GET request or other method, redirect to the home page
    return render_template('index.html')

@app.route('/', methods=['GET'])
def hiWorld():
    return 'Hi World\n'

if __name__ == '__main__':
    app.run(debug=True)
