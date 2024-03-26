import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os

# Load the model
model_path = 'C:/Users/ambar/OneDrive/Documents/nsfw_model-master/nsfw_mobilenet2.224x224.h5'
model = load_model(model_path)

# Function to classify a single image
def classify_image(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return model.predict(preprocess_input(img_array_expanded_dims))

# Define category names
categories = ['Drawings', 'Hentai', 'Neutral', 'Porn', 'Sexy']

# Directory containing images
directory_path = 'C:/Users/ambar/OneDrive/Documents/nsfw_model-master/images/DHS_Image_Folder'

for filename in os.listdir(directory_path):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Check for image files
        image_path = os.path.join(directory_path, filename)
        results = classify_image(image_path, model)
        
        # Match results to categories and print
        print(f"Results for {filename}:")
        for category, score in zip(categories, results[0]):
            print(f" - {category}: {score*100:.2f}%")
