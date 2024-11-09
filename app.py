from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename
from config import IBM_WATSONX_API_KEY, IBM_WATSONX_PROJECT_ID, IBM_WATSONX_URL
from utils.cv_model_utils import predict_image
from utils.allam import IBMWatsonXAIWrapper
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize the wrapper when the app starts
allam = IBMWatsonXAIWrapper(IBM_WATSONX_API_KEY, IBM_WATSONX_PROJECT_ID, IBM_WATSONX_URL)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')

def get_recommendations(user_prompt):
        prompt = f"{user_prompt} اعطني ثلاث اقتراحات للسؤال في هذا الموضوع:"
        generated_text = allam.generate_text(prompt)
        pattern = r'\d+\.\s([^\n]+)'

        # Find all matches
        recommendations = re.findall(pattern, generated_text)

        # Get the first 3 recommendations
        top_recommendations = recommendations[:3]
        return top_recommendations

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Handle the user input prompt
        prompt = request.form.get('prompt')  # Get the user input prompt from the form

        if prompt:
            try:
                # Generate the response text from the AI model
                generated_text = allam.generate_text(prompt)
                
                # Return the generated text as JSON
                return jsonify({'generated_text': generated_text})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'No prompt provided'}), 400
    
    else:
        # Handle image-based request (same as before)
        filename = request.args.get('filename')  # Get the filename from the query parameter
        if filename:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                prediction = predict_image(image_path)  # Get prediction
                image_url = url_for('static', filename=f'uploads/{filename}')
                
                prompt = f"اكتبلي تاريخ {prediction} بشكل مختصر"
                generated_text = allam.generate_text(prompt)
                print(generated_text)

                # Render the result template with the prediction and generated text
                return render_template('result.html', prediction=prediction, image_url=image_url,
                                       generated_text=generated_text)
            except Exception as e:
                return str(e), 500
        return "No image found", 404

@app.route('/recommendation', methods=['POST'])
def recommendation():
    prompt = request.form.get('prompt')  # Get the prompt from the form data

    if prompt:
        try:
            recommendations = get_recommendations(prompt)
            
            # Return the recommendations as JSON
            return jsonify({'recommendations': recommendations})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No prompt provided'}), 400

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
