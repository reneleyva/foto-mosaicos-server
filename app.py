from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from src.mosaico import process_image
from io import BytesIO
from PIL import Image
from src.AVL import AVLTree

from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove
from PIL import Image
from sys import getsizeof
import os

app = Flask(__name__)
range_search_tree = AVLTree()
range_search_tree.fillImageDB("/home/luis/Documents/foto-mosaicos-server/src/BD.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        photo = request.files['photo']
       	im = Image.open(BytesIO(photo.read()))
        process_image(im, range_search_tree)
        new_im = open('/home/luis/Documents/foto-mosaicos-server/src/result.jpg','rb')
        tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
        copyfileobj(new_im,tempFileObj)
        new_im.close()
        tempFileObj.seek(0,0)
        response = send_file(tempFileObj, as_attachment=False, attachment_filename='image.jpg')
        return response