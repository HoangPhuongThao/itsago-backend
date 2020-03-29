import os
import re
from flask import Flask, render_template, url_for, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from object_detection import detect_objects

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/images'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'pXuUdktb5IAHe_xbzqEiCA'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/upload_image", methods=['GET', 'POST'])
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
            filename = secure_filename(file.filename)
            flash('file {} saved'.format(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # detect_objects(filename)
            response = parse_objectname()
            return jsonify(response)
            # return redirect(url_for('upload_image'))
    return render_template('upload_image.html')

@app.route('/searchbar', methods=['POST','GET'])
def searchbar():
  if request.method == 'POST':
      input = request.form['text']
      print(input)
  return render_template('search.html')

def parse_objectname():
    api_response = open("detected_objects.txt", "r")
    lines = api_response.readlines()
    objects = []; scores = []; response = []
    for line in lines:
        if "name" in line:
            object = re.search(r'"(.*?)"', line.split("name: ")[1]).group(1)
            objects.append(object)
        elif "score" in line:
            scores.append(re.match(r'score: (\d+(\.\d+)?)', line).group(1))
    api_response.close()
    for i in range(len(objects)):
        response.append({
            "name": objects[i],
            "score": scores[i]
        })
    return response

if __name__ == '__main__':
    app.run(debug=True)
