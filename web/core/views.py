from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import current_app as app
from werkzeug.utils import secure_filename
from web.tensorflow.image_recognize import recieve_image
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
            predicted_label_index = recieve_image(image_path)
            results.append((filename, predicted_label_index))
    return render_template('results.html', results=results)

@core.route('/correct_result/<image_filename>/<predicted_label>', methods=['POST'])
def correct_result(image_filename, predicted_label):
    corrected_label = request.form['corrected_label']

    # 根据用户输入的物品名称创建文件夹
    target_folder = os.path.join('/srv/image_rec/web/training_data', corrected_label)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 将图片移动到新文件夹中
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    target_path = os.path.join(target_folder, image_filename)
    os.rename(source_path, target_path)

    return render_template('index.html')
