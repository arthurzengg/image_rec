from flask import Flask, render_template, request, redirect, url_for, Blueprint

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/Users/arthurzeng/desktop/tensorflow/image_rec/web/static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

from web.core.views import core

app.register_blueprint(core)

