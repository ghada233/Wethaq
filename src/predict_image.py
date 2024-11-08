import cv2
import numpy as np
import joblib
from tensorflow.keras.models import load_model

def predict_image(image_path, img_size=(224, 224)):
    """
    Predict the class of an image using the trained models.
    
    Parameters:
    - image_path: str, path to the input image.
    - img_size: tuple, target size for resizing the image before prediction (default is (224, 224)).
    
    Returns:
    - prediction: str, predicted class label.
    """

    # Load the VGG model
    VGG_model = load_model('/Users/kamel402/Desktop/Hackathons/ALLAM/Wethaq/models/vgg_model.h5')

    # Load the Random Forest model
    model = joblib.load('/Users/kamel402/Desktop/Hackathons/ALLAM/Wethaq/models/random_forest_model.pkl')

    # Load the label encoder
    le = joblib.load('/Users/kamel402/Desktop/Hackathons/ALLAM/Wethaq/models/label_encoder.pkl')

    # Load and display the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct display
    # plt.show()

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
    prediction_RF = model.predict(input_img_features)[0]

    # Reverse the label encoding to get the original class name
    prediction_RF = le.inverse_transform([prediction_RF])

    # Return the predicted class
    return prediction_RF[0]