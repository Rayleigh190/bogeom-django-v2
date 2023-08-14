from google.cloud import vision
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def ocr(image): # google cloud vision ocr API
  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(BASE_DIR)+'/google_service_secret_key.json'

  # Instantiates a client
  client = vision.ImageAnnotatorClient()

  image = vision.Image(content=image)

  # Performs label detection on the image file
  response = client.text_detection(image=image)
  labels = response.text_annotations
  if(len(labels)==0):
    ocr_result = "fail"
  else: 
    ocr_result = labels[0].description

  return ocr_result