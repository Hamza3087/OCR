from flask import Flask, request, jsonify
import easyocr
import os
from werkzeug.utils import secure_filename

# Initialize the Flask app
app = Flask(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # List of supported languages, 'en' for English

# Set a folder to save uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created upload folder at: {UPLOAD_FOLDER}")
else:
    print(f"Upload folder exists at: {UPLOAD_FOLDER}")

@app.route('/upload', methods=['GET'])
def get_upload():
    """Handle GET requests to the /upload endpoint."""
    print("Received GET request at /upload")
    return jsonify({"message": "Use POST method to upload an image to extract text"})

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle POST requests to upload an image and extract text."""
    print("Received POST request at /upload")

    # Check if the image is in the request
    if 'image' not in request.files:
        print("No 'image' key in request.files")
        return jsonify({"error": "No image part in request. Make sure to send the file with key 'image'"}), 400

    file = request.files['image']
    print(f"File received: {file.filename}")

    # Check if a file is selected
    if file.filename == '':
        print("Empty filename received")
        return jsonify({"error": "No selected file. Ensure the file is uploaded"}), 400

    # Secure the filename and save the image
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Saving file to: {file_path}")
    file.save(file_path)

    # Use EasyOCR to extract text from the image
    try:
        print(f"Starting text extraction for file: {file_path}")
        result = reader.readtext(file_path)
        print(f"Raw OCR result: {result}")

        # Extract text from the result
        extracted_text = " ".join([text[1] for text in result])
        print(f"Extracted text: {extracted_text}")
    except Exception as e:
        print(f"Error during text extraction: {str(e)}")
        return jsonify({"error": f"Text extraction failed: {str(e)}"}), 500

    return jsonify({"extracted_text": extracted_text})

if __name__ == '__main__':
    print("Starting Flask server on http://0.0.0.0:8082")
    app.run(debug=True, host='0.0.0.0', port=8082)
