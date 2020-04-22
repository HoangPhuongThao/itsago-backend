import os
import re
import string
import random
from flask import Flask, render_template, url_for, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from object_detection import detect_objects
from database import match, get_all
from synonyms import get_synonyms, find_syns_db
import feedback

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/images'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'pXuUdktb5IAHe_xbzqEiCA'

@app.route("/api/test")
def hello():
    response = ["nothing found"]
    return jsonify(response)


@app.route("/api/home")
def home():
    return render_template('home.html')

@app.route("/api/upload_image", methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith(('.png', '.jpg', '.jpeg')):
            filename = random_generator() + os.path.splitext(file.filename)[1]
            flash('file {} saved'.format(filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            detect_objects(filename)
            os.remove(os.path.abspath('images/' + filename))
            response = parse_objectname()
            if not response:
                response = ["nothing found"]
            return jsonify(response)
    return render_template('upload_image.html')

@app.route('/api/searchbar', methods=['POST','GET'])
def searchbar():
    if request.method == 'GET':
        input = request.args.get('text')
        syns = get_synonyms(input)
    return find_syns_db(syns)

@app.route('/api/suggest', methods=['POST','GET'])
def suggest():
    if request.method == 'GET':
        substring = request.args.get('text')
        suggestions = match(substring, match_whole_substring=False) # only match words starting with the substring
        return suggestions

@app.route('/api/feedback', methods=['POST', 'GET'])
def add_feedback():
    if request.method == 'POST':
        rank = request.form.get('nb_stars')
        text = request.form.get('feedback')
        feedback.process_feedback(rank, text)
        return 'feedback processed', 201
    else:
        return 'bad request', 400

@app.route('/api/suggest_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'GET':
        text = request.args.get('item')
        feedback.process_unfound_item(text)
        return 'item added', 201
    else:
        return 'bad request', 400

@app.route('/api/get_feedback', methods=['GET'])
def get_feedback():
    return feedback.retrieve_all('rank_feedback'), 200

@app.route('/api/get_suggested_items', methods=['GET'])
def get_suggestions():
    return feedback.retrieve_all('notfound_feedback'), 200

def parse_objectname():
    api_response = open("detected_objects.txt", "r")
    lines = api_response.readlines()
    objects = []; scores = []; response = []
    skip_score = False
    for line in lines:
        if "description" in line:
            object = re.search(r'"(.*?)"', line.split("description: ")[1]).group(1)
            if object not in objects:
                objects.append(object)
                skip_score = False
            else: skip_score = True
        elif skip_score == False and "score" in line:
            scores.append(re.match(r'score: (\d+(\.\d+)?)', line).group(1))
    api_response.close()
    for i in range(len(objects)):
        response.append({
            "name": objects[i],
            "score": scores[i]
        })
    return response

def random_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    app.run(debug=True)
