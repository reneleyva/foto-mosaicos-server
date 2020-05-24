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

range_search_tree_small = AVLTree()
range_search_tree_medium= AVLTree()
range_search_tree_20 = AVLTree()

range_search_tree_small.fillImageDB(10)
range_search_tree_medium.fillImageDB(15)
# range_search_tree_large.fillImageDB(30)

print("Árboles construidos.")

@app.route('/home')
def form():
    return render_template('index.html')

def get_tree_and_size (size):
    (size_x, size_y) = size
    resolution = size_x * size_y
    # if resolution > 10000000:
    #     return range_search_tree_large,30
    if resolution > 1000000:
        return range_search_tree_medium,15
    return range_search_tree_small,10

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        photo = request.files['photo']
       	im = Image.open(BytesIO(photo.read()))
        tree, size = get_tree_and_size(im.size)
        process_image(im, tree,size)
        new_im = open('/home/luis/Documents/foto-mosaicos-server/src/result.jpg','rb')
        tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
        copyfileobj(new_im,tempFileObj)
        new_im.close()
        tempFileObj.seek(0,0)
        response = send_file(tempFileObj, as_attachment=True, attachment_filename='result.jpg')
        return response

@app.route('/image', methods=['GET'])
def get_simple_image():
    if request.method == 'GET':
        img = open(os.environ.get("SAMPLE_IMAGE_PATH"),'rb')
        tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
        copyfileobj(img,tempFileObj)
        img.close()
        tempFileObj.seek(0,0)
        response = send_file(tempFileObj, as_attachment=False, attachment_filename='image.jpg')
        return response

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
        
