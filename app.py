from flask import Flask, render_template, request
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
        return render_template('results.html', search_input = search_query)
    # If it's a GET request or other method, redirect to the home page
    return render_template('index.html', search_input = '')

if __name__ == '__main__':
    app.run(debug=True)
