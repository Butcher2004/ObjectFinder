


# flask-backend/app.py
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
import base64
from io import BytesIO
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to the assets folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURRENT_DIR)
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, '..', 'src', 'assets')
print(UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload/<name>', methods=['POST'])
def upload_file(name):
    if name not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files[name]
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, name+".jpg")
    file.save(filepath)
    return jsonify({"message": "File uploaded successfully", "filepath": filepath}), 200





# @app.route('/generate', methods=['POST'])
# def generate():
#     if 'query' not in request.form:
#         return jsonify({"error": "No query part"}), 400
    
#     to_detect = request.form['query'].split(" ")
#     print(to_detect)

#     # Step 1: Load the image from local storage
#     image_path = r"E:\Projects\Obj_DET\object_detection\src\assets\original.jpg"
#     image = Image.open(image_path).convert("RGB")  # Convert image to RGB mode

#     # Step 2: Set up the object detection pipeline
#     detector = pipeline(model="google/owlvit-base-patch32", task="zero-shot-object-detection")
#     results = detector(image, candidate_labels=to_detect)

#     # Step 3: Draw the bounding boxes on the image
#     font_size = 20
#     font = ImageFont.truetype("arial.ttf", font_size)
#     draw = ImageDraw.Draw(image)
#     if len(results) == 0:
#         return jsonify({"message": "No objects detected", "detected": False}), 200
#     for result in results:
#         # print(result)
#         box = result['box']
#         draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=5)
#         draw.text((box['xmin'], box['ymin'] - font_size), result['label'].capitalize(), fill="blue", font=font)

#     # Save the image with bounding boxes
#     # output_path = r"E:\Projects\Obj_DET\object_detection\src\assets\detected.jpg"
#     # image.save(output_path, format="JPEG")

#     buffered = BytesIO()
#     image.save(buffered, format="JPEG")
#     img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
#     # Return a success response
#     return jsonify({"message": "Image processed successfully", 'detected': True, "image": img_str}), 200






@app.route('/generate', methods = ['POST'])
def generate():
    if 'query' not in request.form:
        return jsonify({"error": "No query part"}), 400
    
    to_detect = request.form['query'].split(" ")
    print(to_detect)
    print("Request : ",request.form)
    qimage = request.form['qimage']
    image_path = r"E:\Projects\Obj_DET\object_detection\src\assets\original.jpg"
    image = Image.open(image_path).convert("RGB")

    #model
    checkpoint = "google/owlvit-base-patch32"
    model = AutoModelForZeroShotObjectDetection.from_pretrained(checkpoint)
    processor = AutoProcessor.from_pretrained(checkpoint)
    #model
    print("Qimage : ",qimage)
    print()
    if qimage=='1':
        query_image_path = r"E:\Projects\Obj_DET\object_detection\src\assets\qimage.jpg"
        query_image = Image.open(query_image_path).convert("RGB") 

        inputs = processor(images=image, query_images=query_image, return_tensors="pt")
        with torch.no_grad():
            outputs = model.image_guided_detection(**inputs)
            target_sizes = torch.tensor([image.size[::-1]])
            results = processor.post_process_image_guided_detection(outputs=outputs, target_sizes=target_sizes)[0]

        # print(results)
        draw = ImageDraw.Draw(image)

        scores = results["scores"].tolist()
        boxes = results["boxes"].tolist()

        print("Scores : ",scores)

        for box, score in zip(boxes, scores):
            if(score>0.7):
                print("Detected Scores : ",score)
                xmin, ymin, xmax, ymax = box
                draw.rectangle((xmin, ymin, xmax, ymax), outline="white", width=4)
        print("If loop executed")
    
    else:
        
        inputs = processor(text=to_detect, images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            target_sizes = torch.tensor([image.size[::-1]])
            results = processor.post_process_object_detection(outputs, threshold=0.1, target_sizes=target_sizes)[0]

        # print("Results : " , results)
        # print("type : ",type(results))

        scores = results["scores"].tolist()
        labels = results["labels"].tolist()
        boxes = results["boxes"].tolist()

        if len(labels) == 0:
            return jsonify({"message": "No objects detected", "detected": False}), 200
        print("Labels_num : " , len(labels))

        font_size = 20
        font = ImageFont.truetype("arial.ttf", font_size)
        draw = ImageDraw.Draw(image)

        for box, score, label in zip(boxes, scores, labels):
            xmin, ymin, xmax, ymax = box
            draw.rectangle((xmin, ymin, xmax, ymax), outline="blue", width=2)
            draw.text((xmin, ymin-font_size), f"{to_detect[label].capitalize()}", fill="black", font=font)



    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # Return a success response
    return jsonify({"message": "Image processed successfully", 'detected': True, "image": img_str}), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)

