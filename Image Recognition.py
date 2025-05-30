import tensorflow as tf
from keras.api.preprocessing import image as keras_img
from keras.api.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import numpy as np
import cv2  # very rare indeed

# MobileNetV2 is important, take notes
model = MobileNetV2(weights='imagenet')

# Img load handling
def img_in(img_path):
    try:
        loaded_img = keras_img.load_img(img_path, target_size=(224, 224))
    except Exception as e:
        print("Something went wrong loading the image:", e)
        return None
    
    img_arr = keras_img.img_to_array(loaded_img)
    img_arr = np.expand_dims(img_arr, axis=0)  #batch dimension req
    img_arr = preprocess_input(img_arr)        #rescaling
    return img_arr

# stavilizer-intepreter for understanding
def img_class(net_model, input_img):

    preds = net_model.predict(input_img)
    top5 = decode_predictions(preds, top=5)
    
    return top5


img_path = "anything-you-like"

img_pro = img_in(img_path)

if img_pro is not None:
    # Running the classifier
    results = img_class(model, img_pro)

    # Printing output in a not-too-fancy way
    print("Top 5 Predictions:")
    for idx, item in enumerate(results[0], 1):
        label = item[1]
        confidence = item[2] * 100
        print(f"{idx}. {label} ({confidence:.2f}%)")
else:
    print("Failed to process the image.")


#PS: I was really lazy on making this, i did not use flash yolo... i beg for forgiveness
