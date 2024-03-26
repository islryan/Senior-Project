import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Load the model
model_path = 'C:/Users/ambar/OneDrive/Documents/nsfw_model-master/nsfw_mobilenet2.224x224.h5'
model = load_model(model_path)

# Function to classify a single image
def classify_image(image_path, model):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return model.predict(preprocess_input(img_array_expanded_dims))
'''
# Example usage with a single image
image_path = 'C:/Users/ambar/OneDrive/Documents/nsfw_model-master/images/DHS_Image_Folder/your_image.jpg' # Update this path to an actual image
results = classify_image(image_path, model)
print(results)
'''

# If you want to classify multiple images in a directory
import os

directory_path = 'C:/Users/ambar/OneDrive/Documents/nsfw_model-master/images/DHS_Image_Folder' # Update this path to your directory

for filename in os.listdir(directory_path):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Add any file extensions of interest
        image_path = os.path.join(directory_path, filename)
        results = classify_image(image_path, model)
        print(f"Results for {filename}: {results}")
