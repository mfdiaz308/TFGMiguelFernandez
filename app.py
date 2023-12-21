import json
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_course(query):
    with open('test.json','r') as f:
        data = json.load(f)

    for course in data:
        if query.lower() in course['name'].lower() or query.lower() in course['skills'] or query.lower() in course['description']:
            print(str(course['name']))
            return course
    
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search']
        print("Search query:", search_query)
        course = get_course(search_query)
        # Redirects back to the home page for now
        return render_template('results.html', course_url = course['url'], course_name = course['name'])
    # If it's a GET request or other method, redirect to the home page
    return render_template('index.html', search_input = '')

#TODO: setup apache server
#TODO: put all json files in one file
#TODO: display search_query directly when switching to results.html

if __name__ == '__main__':
    app.run(debug=True)
