from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from io import BytesIO
import numpy as np

app = Flask(__name__)

# Load the model
model = load_model('C:/Users/ambar/OneDrive/Documents/nsfw_model-master/nsfw_mobilenet2.224x224.h5')

# Define the categories detected by the model
categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

@app.route('/')
def index():
    # This route is for testing if the server is running
    return "The Server For Running the NSFW Classifier Mobile App is Active VIA Flask."

@app.route('/classify', methods=['POST'])
def classify_image():
    # This route is for handling image classification
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Convert the file stream to a BytesIO object
    file_bytes = BytesIO(file.stream.read())
    img = image.load_img(file_bytes, target_size=(224, 224))

    # Preprocess the image
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make the prediction
    predictions = model.predict(img_array)

    # Convert decimal probabilities to percentages and pair with category labels
    results = [{"Category": category, "Percentage": float(probability) * 100} for category, probability in zip(categories, predictions[0])]

    return jsonify({"predictions": results})

if __name__ == '__main__':
    # This will run the server accessible on your local network
    app.run(debug=True, host='0.0.0.0')
