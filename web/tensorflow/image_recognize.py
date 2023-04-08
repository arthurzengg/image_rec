import tensorflow as tf
import numpy as np
from PIL import Image

def load_labels(file_path):
    with open(file_path, "r") as f:
        label_list = f.readlines()
        labels = [label.strip() for label in label_list]
    return labels

def preprocess_image(image_path, input_shape):
    image = Image.open(image_path)
    image = image.resize(input_shape)
    image_array = np.array(image, dtype=np.uint8)
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def predict_image(model_path, image_array, labels):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]["index"], image_array)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]["index"])
    top_prediction = np.argmax(output_data)
    return labels[top_prediction]

def recieve_image(image_path):
    model_path = "/Users/arthurzeng/desktop/tensorflow/image_rec/web/tensorflow/model.tflite"
    label_map_path = "/Users/arthurzeng/desktop/tensorflow/image_rec/web/tensorflow/labels.txt"

    # Load labels
    labels = load_labels(label_map_path)

    # Load and preprocess image
    input_shape = (224, 224)  # Change this to match your model's input shape
    image_array = preprocess_image(image_path, input_shape)

    # Predict image
    prediction = predict_image(model_path, image_array, labels)
    # print(f"Predicted item in the image: {prediction}")
    return prediction

