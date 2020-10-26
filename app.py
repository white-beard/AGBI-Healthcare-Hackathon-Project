import requests 
from flask import Flask
import os
import sys
import json

upload_folder = "uploads"

url = "http://localhost:5000/predict"

image_path = os.path.join( upload_folder, os.listdir(upload_folder)[0] )   

image = open(image_path, "rb").read()
payload = {"image" : image}
os.remove(image_path)
r = requests.post(url, files = payload).json()

preds = json.dumps(r)
with open("prediction.json", 'w+') as file:
    file.write(preds)
print(r)
sys.stdout.flush()