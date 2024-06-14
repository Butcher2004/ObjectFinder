


# flask-backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to the assets folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURRENT_DIR)
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, '..', 'src', 'assets')
print(UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, "original.jpg")
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filepath": filepath}), 200





@app.route('/generate', methods=['POST'])
def generate():
    if 'query' not in request.form:
        return jsonify({"error": "No query part"}), 400
    
    to_detect = request.form['query'].split(" ")
    print(to_detect)

    # Step 1: Load the image from local storage
    image_path = r"E:\Projects\Obj_DET\object_detection\src\assets\original.jpg"
    image = Image.open(image_path).convert("RGB")  # Convert image to RGB mode

    # Step 2: Set up the object detection pipeline
    detector = pipeline(model="google/owlvit-base-patch32", task="zero-shot-object-detection")
    results = detector(image, candidate_labels=to_detect)

    # Step 3: Draw the bounding boxes on the image
    font_size = 20
    font = ImageFont.truetype("arial.ttf", font_size)
    draw = ImageDraw.Draw(image)
    if len(results) == 0:
        return jsonify({"message": "No objects detected", "detected": False}), 200
    for result in results:
        # print(result)
        box = result['box']
        draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=5)
        draw.text((box['xmin'], box['ymin'] - font_size), result['label'].capitalize(), fill="blue", font=font)

    # Save the image with bounding boxes
    # output_path = r"E:\Projects\Obj_DET\object_detection\src\assets\detected.jpg"
    # image.save(output_path, format="JPEG")

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # Return a success response
    return jsonify({"message": "Image processed successfully", 'detected': True, "image": img_str}), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)

