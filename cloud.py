import os
import sys

from cloudinary.api import delete_resources_by_tag, resources_by_tag, resources
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from PIL import Image
import requests
from io import BytesIO


def get_resources():
    response = resources(type = "upload", max_results = 5000)

    for item in response["resources"]:
        if item["bytes"] > 0:
            print(item["url"])

def create_images():
    n = 20

    for i in range (16777216):

        if i%(16777216//n) == 0:

            R = i%256
            G = (i//256)%256
            B = (i //65536)%256
            print(R,G,B)
            img = Image.new('RGB', (250,250), (R, G, B))
            img.save(f'colors/{R}-{G}-{B}', "JPEG")


create_images()