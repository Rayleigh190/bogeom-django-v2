import os, json
import openai


from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


OPENAI_KEY = get_secret("OPENAI_KEY")


def chatGPT(ocr_result): # cahtGPT API
  openai.api_key = OPENAI_KEY
  try:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "user",
          "content": str(ocr_result) + "Extract one product name from this list. Also tell me the index of that element. Respond in the following JSON format. {\"index\": number,\"product_name\":\"product name\"} . If extraction fails, respond with: {\"product_name\":\"fail\"}"
        }
      ],
    )
  except Exception as e:
    print('ChatGPT 예외가 발생했습니다.', e)

  decoded = completion.choices[0].message["content"]
  return decoded