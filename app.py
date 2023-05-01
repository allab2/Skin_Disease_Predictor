import logging
import os

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request
from PIL import Image

app = Flask(__name__)
model_path = os.path.join(os.getcwd(), "skin_disease.tflite")
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

class_names = [
    "Acne and Rosacea Photos",
    "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions",
    "Atopic Dermatitis Photos",
    "Bullous Disease Photos",
    "Cellulitis Impetigo and other Bacterial Infections",
    "Eczema Photos",
    "Exanthems and Drug Eruptions",
    "Hair Loss Photos Alopecia and other Hair Diseases",
    "Herpes HPV and other STDs Photos",
    "Light Diseases and Disorders of Pigmentation",
    "Lupus and other Connective Tissue diseases",
    "Melanoma Skin Cancer Nevi and Moles",
    "Nail Fungus and other Nail Disease",
    "Poison Ivy Photos and other Contact Dermatitis",
    "Psoriasis pictures Lichen Planus and related diseases",
    "Scabies Lyme Disease and other Infestations and Bites",
    "Seborrheic Keratoses and other Benign Tumors",
    "Systemic Disease",
    "Tinea Ringworm Candidiasis and other Fungal Infections",
    "Urticaria Hives",
    "Vascular Tumors",
    "Vasculitis Photos",
    "Warts Molluscum and other Viral Infections",
]
size = (48, 48)

@app.route('/')
def index():
    return "<div class='container'><h1>Hi There</h1></div>"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        print('fxn started')
        print("request: " + str(request.files.to_dict().get('image', None)))
        # Load the image file from the request object
        image_file = request.files.to_dict().get('image', None)
        image = Image.open(image_file).convert("L").resize(size)

        # Convert the image to a numpy array
        image_array = np.array(image)

        print('image array created: ' + str(image_array))

        # Reshape the array to match the expected input shape of the model
        image_array = image_array.reshape((*size, 1))

        # Normalize the pixel values to be between 0 and 1
        image_array = image_array / 255.0

        # Make the prediction using the model
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], np.array([image_array], dtype=np.float32))
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]['index'])

        print('prediction: ' + str(prediction))

        # Get the predicted label and return it as a response
        label = int(np.argmax(prediction))
        accuracy = float(np.max(prediction))
        disease_name = class_names[label]
        response = {"label": label, "accuracy": accuracy, "disease_name": disease_name}

        print('response: ' + str(response))

        logging.info(f"Prediction: {disease_name} (Accuracy: {accuracy})")
        return jsonify({
            "label": label, 
            "accuracy": accuracy, 
            "disease_name": disease_name
            })

    except Exception as e:
        logging.error(str(e))
        print("Error: " + str(e))
        return jsonify({"error": str(e)})
    

if __name__ == "__main__":
    app.run(debug=True)


