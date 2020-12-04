from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_file,
    url_for
)
from src.mosaico import process_image
from src.promedio import fill_db as fill_db_file
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

AVAILABLE_SIZES = [5,10,12,15,18,20,25]

tree = AVLTree()
# tree.fillImageDB(AVAILABLE_SIZES)

@app.route('/home')
def form():
    return render_template('index.html')

def get_size(size):
    x,y = size

    total_size = x*y

    mosaic_size = (.010*total_size)**.5

    count = 0

    while count < (len(AVAILABLE_SIZES) - 1) and mosaic_size > AVAILABLE_SIZES[count]:
        count += 1

    return AVAILABLE_SIZES[count]


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        photo = request.files['photo']
       	im = Image.open(BytesIO(photo.read()))
        size = get_size(im.size)
        process_image(im, tree, size)
        new_im = open('/home/luis/Documents/foto-mosaicos-server/src/result.jpg','rb')
        tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
        copyfileobj(new_im,tempFileObj)
        new_im.close()
        tempFileObj.seek(0,0)
        response = send_file(tempFileObj, as_attachment=False, attachment_filename='result.jpg')
        return response

@app.route('/fill_db', methods=['GET'])
def fill_db():
    fill_db_file()
    return redirect(url_for('home'))

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/template', methods=['GET'])
def template():
    return render_template('template.html')



# @app.route('/image', methods=['GET'])
# def get_simple_image():
#     if request.method == 'GET':
#         img = open("./src/image.png")
#         tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
#         copyfileobj(img,tempFileObj)
#         img.close()
#         tempFileObj.seek(0,0)
#         response = send_file(tempFileObj, as_attachment=False, attachment_filename='image.jpg')
#         return response
        
