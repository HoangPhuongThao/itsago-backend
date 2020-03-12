import io
import os
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'auth.json'

def detect_objects(filename):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath('images/' + filename)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    with open('labels.txt', 'w') as outfile:
        outfile.write(str(labels))

    print('Labels:')
    for label in labels:
        print(label.description)
