from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from src.predict_image import predict_image
from src.ALLAM import IBMWatsonXAIWrapper

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize the IBM WatsonX AI Wrapper
api_key = os.getenv("IBM_WATSONX_API_KEY") or 't7YJ-yWRGikWjOtoJ6TSBpWcDvUBldkDHHbyMtOyhq7Q'
project_id = os.getenv("IBM_WATSONX_PROJECT_ID") or 'a29156ce-b814-46b8-aa88-a21e0243a084'
url = os.getenv("IBM_WATSONX_URL", "https://eu-de.ml.cloud.ibm.com")
wrapper = IBMWatsonXAIWrapper(api_key, project_id, url)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@app.route('/FAQs')
def FAQs():
    return render_template('FAQs.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    print(request.method)
    print(request.files)
    if request.method == 'POST':
        # Handle the file upload
        
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Secure the filename and save the image
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(file_path)


            # Make the prediction for the uploaded image (you should implement your image prediction logic)
            # prediction = "Prediction result here"
            prediction = predict_image(file_path)  # Get prediction

            # Call WatsonX to generate text based on the prediction
            prompt = f"اكتبلي تاريخ {prediction} بشكل مختصر"
            generated_text = wrapper.generate_text(prompt)
            print(generated_text)
            # Render the result template with the prediction and generated text
            return render_template('result.html', prediction=prediction,image_url=file_path, generated_text=generated_text)

    return redirect(url_for('index'))

@app.route('/result')
def result():
    filename = request.args.get('filename')  # Get the filename from the query parameter
    if filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            prediction = predict_image(image_path)  # Get prediction
            image_url = url_for('static', filename=f'uploads/{filename}')


            prompt = f"اكتبلي تاريخ {prediction} بشكل مختصر"
            generated_text = wrapper.generate_text(prompt)
            print(generated_text)
            # Render the result template with the prediction and generated text
            return render_template('result.html', prediction=prediction,image_url=image_url, generated_text=generated_text)
        except Exception as e:
            return str(e), 500
    return "No image found", 404


@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Redirect to the result page, passing the filename as a query parameter
            return redirect(url_for('result', filename=filename))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

