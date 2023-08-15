from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status
from search.models import Item, Market, MarketItems
from .myViews.myNaver import NaverMap
from .myViews import myGPS
from pprint import pprint as pp

def set_dic(market_name, market_lat, market_lon, market_addr, item_name, item_price, item_updated):
  dic = {
    "market_name": market_name,
    "market_coords": {
      "lat": market_lat,
      "lon": market_lon,
    },
    "market_address": market_addr,
    "shop_logo": None, # 빼기
    "item":{
      "item_name": item_name,
      "item_price": item_price,
      "updated_at": item_updated
    }
  }
  return dic


class SearchMarketView(APIView):
    
  def get(self, request):
    item_id = request.GET['id']
    map_lat = request.GET['lat']
    map_lon = request.GET['lon']

    coords = f"{map_lon},{map_lat}"
    naver_map = NaverMap() 
    gc_res = naver_map.gc(coords) # 좌표를 주소로 변환
    addr = "" # 지도 위치의 도로명주소
    area1_name = gc_res['results'][0]['region']['area1']['name']
    area2_name = gc_res['results'][0]['region']['area2']['name']
    # area3_name = gc_res['results'][0]['region']['area3']['name']
    # area4_name = gc_res['results'][0]['region']['area4']['name']
    addr = f"{area1_name} {area2_name.split(' ')[0]} "

    markets = Market.objects.filter(road_address__contains=addr)

    near_market_list = []
    for market in markets:
      dis = myGPS.haversine_distance(float(map_lat), float(map_lon), market.latitude, market.longitude)
      if dis <= 0.7: # 거리가 700m 이내이면
        near_market_list.append(market)
    
    # print(near_market_list)
    near_market_item_list = []
    for near_market in near_market_list:
      try:
        market_item  = MarketItems.objects.get(market_id=near_market.id, item_id=item_id)
        item = Item.objects.get(id=market_item.item_id.id)
        dic = set_dic(near_market.market_name, near_market.latitude, near_market.longitude, near_market.road_address, item.item_name, market_item.item_price, market_item.updated_at)

        near_market_item_list.append(dic)
      except Exception as e:
        # print(e)
        pass # 마켓에 id에 해당하는 상품이 없으면 패스
    # pp(near_market_item_list)
    
    final_result_dic = {
      'success': True, 
      'response': {
        'markets': near_market_item_list
      },
      'error': None
    }

    return Response(final_result_dic)
  
