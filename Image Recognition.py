import tensorflow as tf
from keras.api.preprocessing import image
from keras.api.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np
import cv2

# Load the MobileNetV2 model pre-trained on ImageNet
model = MobileNetV2(weights='imagenet')

# Load and preprocess the image
def load_and_preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# Predict the class of the image
def predict_image_class(model, preprocessed_image):
    predictions = model.predict(preprocessed_image)
    decoded_predictions = decode_predictions(predictions, top=5)
    return decoded_predictions

# Path to the image
image_path = "C:/Users/dipra/Downloads/Sigma.jpg"

# Load and preprocess the image
preprocessed_image = load_and_preprocess_image(image_path)

# Predict the class of the image
predictions = predict_image_class(model, preprocessed_image)

# Print the top 5 predictions
print("Top 5 Predictions:")
for i, prediction in enumerate(predictions[0], start=1):
    print(f"{i}. {prediction[1]} ({prediction[2]*100:.2f}%)")
