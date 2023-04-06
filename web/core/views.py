from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import current_app as app
from werkzeug.utils import secure_filename
from PIL import Image
import os

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@core.route('/upload', methods=['POST'])
def upload():
    if 'images' not in request.files:
        return redirect(request.url)
    images = request.files.getlist('images')
    results = []
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            # predicted_label_index = predict(image_path)
            # results.append((filename, predicted_label_index))
    return render_template('results.html')