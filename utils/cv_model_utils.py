import cv2
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import os

# Global variables to hold the models
VGG_model = None
random_forest_model = None
label_encoder = None


def load_models():
    """
    Load the pre-trained models once and store them globally.
    """
    global VGG_model, random_forest_model, label_encoder

    if VGG_model is None:
        # Load the VGG model
        VGG_model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'vgg_model.h5')
        VGG_model = load_model(VGG_model_path)
        print("VGG model loaded.")

    if random_forest_model is None:
        # Load the Random Forest model
        random_forest_model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'random_forest_model.pkl')
        random_forest_model = joblib.load(random_forest_model_path)
        print("Random Forest model loaded.")

    if label_encoder is None:
        # Load the label encoder
        le_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'label_encoder.pkl')
        label_encoder = joblib.load(le_path)
        print("Label encoder loaded.")


def predict_image(image_path, img_size=(224, 224)):
    """
    Predict the class of an image using the trained models.

    Parameters:
    - image_path: str, path to the input image.
    - img_size: tuple, target size for resizing the image before prediction (default is (224, 224)).

    Returns:
    - prediction: str, predicted class label.
    """
    # Ensure models are loaded
    load_models()

    # Load and display the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Resize the image to the input size of the model
    img = cv2.resize(img, img_size)

    # Normalize the image
    img = img / 255.0

    # Expand the dimensions to match the input shape of the model
    input_img = np.expand_dims(img, axis=0)

    # Get features using the VGG model
    input_img_feature = VGG_model.predict(input_img)

    # Flatten the feature vector
    input_img_features = input_img_feature.reshape(input_img_feature.shape[0], -1)

    # Predict using the Random Forest model
    prediction_RF = random_forest_model.predict(input_img_features)[0]

    # Reverse the label encoding to get the original class name
    prediction_RF = label_encoder.inverse_transform([prediction_RF])

    # Return the predicted class
    return prediction_RF[0]
