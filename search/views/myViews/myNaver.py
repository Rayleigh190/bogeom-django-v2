import hashlib
import hmac
import base64
import time
import urllib.parse
import urllib.request
import ssl
import json
import os
import requests
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


class NaverMap():
    
  # API KEY
  # api_key = get_secret("NCP_GATEWAY_KEY")

  # 인증 KEY

  # NCP 콘솔에서 복사한 클라이언트ID와 클라이언트Secret 값
  ncp_client_id = get_secret("NCP_CLIENT_ID")
  ncp_client_secret = get_secret("NCP_CLIENT_SECRET")
  
  nd_client_id = get_secret("ND_CLIENT_ID")
  nd_client_secret = get_secret("ND_CLIENT_SECRET")
  

  def gc(self, coords):
    orders = "legalcode,admcode,addr,roadaddr"
    output = "json"

    # API 호출 경로
    endpoint = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    url = f"{endpoint}?coords={coords}&orders={orders}&output={output}"

    # 헤더
    headers = {
      "X-NCP-APIGW-API-KEY-ID": self.ncp_client_id,
      "X-NCP-APIGW-API-KEY": self.ncp_client_secret
    }

    # 요청
    res = requests.get(url, headers=headers)
    # print(res.json())
    return res.json()


  # 네이버 지역 검색
  def local_search(self, query):
    query = urllib.parse.quote(query)
    display = "5"
    url = "https://openapi.naver.com/v1/search/local.json?query=" + query + "&display=" + display
    
    client_id = self.nd_client_id
    client_secret = self.nd_client_secret

    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)

    try:
      response = urllib.request.urlopen(request)
      response_dic = json.loads(response.read().decode('utf-8'))
      return response_dic
    except Exception as e:
      print("네이버 지역검색 API 오류 발생.", e)