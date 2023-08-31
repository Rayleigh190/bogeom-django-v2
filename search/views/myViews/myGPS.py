from .myNaver import NaverMap
from pprint import pprint as pp
import sys
import math
import pyproj
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# 두 wgs84 좌표 사이의 거리 구하기
def haversine_distance(lat1, lon1, lat2, lon2):
  R = 6371.0  # 지구의 반지름 (단위: km)

  lat1_rad = math.radians(lat1)
  lon1_rad = math.radians(lon1)
  lat2_rad = math.radians(lat2)
  lon2_rad = math.radians(lon2)

  dlon = lon2_rad - lon1_rad
  dlat = lat2_rad - lat1_rad

  a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

  distance = R * c  # 두 지점 사이의 거리 (단위: km)
  # print(distance)
  return distance

# katec 좌표를 wgs84 좌표로 변환
def katec_to_wgs84(x, y):
  WGS84 = pyproj.CRS('EPSG:4326')  # WGS84 좌표계
  KATEC = pyproj.CRS(proj='tmerc', lat_0='38N', lon_0='128E', ellps='bessel', x_0='400000', y_0='600000', k='0.9999', units='m', towgs84='-115.80,474.99,674.11,1.16,-2.31,-1.63,6.43')

  transformer = pyproj.Transformer.from_crs(KATEC, WGS84, always_xy=True)
  lon, lat = transformer.transform(x, y)

  return lat, lon

# 소수점 없이 문자열로 된 wgs84 좌표를 실수로 변환하기
def convert_to_real_number(x, y):
  lat = float(x[:2]+'.'+x[2:])
  lon = float(y[:3]+'.'+y[3:])

  return lat, lon


# 사용자의 GPS 좌표
# client_lat = 37.2503798
# client_lon = 127.0347713
# client_lat = 37.2509992
# client_lon = 127.0364095

def get_shop_info(client_lat, client_lon):

  coords = f"{client_lon},{client_lat}"

  gc_res = NaverMap().gc(coords) # 좌표를 주소로 변환

  addr = "" # 사용자 위치의 도로명주소
  area1_name = gc_res['results'][0]['region']['area1']['name']
  area2_name = gc_res['results'][0]['region']['area2']['name']
  area3_name = gc_res['results'][0]['region']['area3']['name']
  area4_name = gc_res['results'][0]['region']['area4']['name']

  try:
    land_name = gc_res['results'][3]['land']['name']
    land_number1 = gc_res['results'][3]['land']['number1']
    addr = f"{area1_name} {area2_name} {area3_name}{area4_name} {land_name} {land_number1}"
  except Exception as e:
    print("도로명 주소 얻기 실패", e)
    area1_name = gc_res['results'][1]['region']['area1']['name']
    area2_name = gc_res['results'][1]['region']['area2']['name']
    area3_name = gc_res['results'][1]['region']['area3']['name']
    area4_name = gc_res['results'][1]['region']['area4']['name']
    addr = f"{area1_name} {area2_name} {area3_name}{area4_name}"

  print("사용자 주소: "+addr+'\n')

  # 사용자가 있는 도로명 주소로 마트, 편의점 검색
  query = addr + " 마트"
  mart_res = NaverMap().local_search(query)
  query = addr + " 편의점"
  conven_res = NaverMap().local_search(query)
  # pp(mart_res)
  # pp(conven_res)

  shop_list = []

  for mart in mart_res['items']:
    if mart['category']=='쇼핑,유통>슈퍼,마트':
      shop_list.append(mart)
  for conven in conven_res['items']:
    if conven['category']=='생활,편의>편의점':
      shop_list.append(conven)

  shortest_shop = {'shop':'', 'dis': sys.maxsize}
  # print(shop_list)
  # 사용자 위치에서 가장 가까운 마트 또는 편의점을 찾아냄
  for shop in shop_list:
    shop_lat, shop_lon = convert_to_real_number(shop['mapy'], shop['mapx'])
    dis = haversine_distance(client_lat, client_lon, shop_lat, shop_lon)
    # print(dis)
    if shortest_shop['dis'] > dis:
      shortest_shop['shop'] = shop
      shortest_shop['dis'] = dis

  shortest_shop['shop']['mapx'], shortest_shop['shop']['mapy'] = int(shortest_shop['shop']['mapx']), int(shortest_shop['shop']['mapy'])
  shortest_shop['shop']['title'] = cleanhtml(shortest_shop['shop']['title'])

  # pp(shortest_shop)
  return shortest_shop