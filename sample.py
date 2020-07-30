from PIL import Image
import requests
from io import BytesIO

url = "http://res.cloudinary.com/luispuli2/image/upload/v1591663106/sample.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()