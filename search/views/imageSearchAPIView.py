from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import json
from .myViews import myGoogle, myOpenai, myFunctions, myGPS
import urllib.parse
from pprint import pprint as pp
from search.models import Market, MarketItems, Item
from search.serializers.serializers import MarketCreateSerializer, ItemCreateSerializer, MarketItemsCreateSerializer
from difflib import SequenceMatcher

def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()


class ImageSearchView(APIView):
    
  def post(self, request):
    client_lat = float(request.POST['lat'])
    client_lon = float(request.POST['lon'])
    shop = myGPS.get_shop_info(client_lat, client_lon)['shop']
    pp(shop)
    print('\n')

    # OCR 진행
    req_img = request.FILES['image']
    pil_image = Image.open(req_img)
    image_bytes = myFunctions.image_to_byte_array(pil_image)
    ocr_result = myGoogle.ocr(image_bytes)
    print("> 1차 ocr 결과: \n" + str(ocr_result)+'\n')

    # Parsing 진행
    split_result_list = ocr_result.split('\n')
    gpt_result = myOpenai.chatGPT(split_result_list)
    dic_result = json.loads(gpt_result)
    print("> ner 결과: " + str(dic_result)+'\n')
    item_name = dic_result['product_name']
    encoded_item_name = urllib.parse.quote(item_name)

    if item_name == 'fail':
      final_result_dic = {'success':False, 'error': '상품명 추출 실패'}
      return Response(final_result_dic)
    
    # item_price = myFunctions.get_pd_price(split_result_list, dic_result['index']) # 가격 추출
    item_price = myFunctions.get_pd_price(split_result_list) # 가격 추출
    if item_price == 'fail':
      item_price = 0

    market_id = 0
    item_id = 0

    try:
      # Market이 있는지 확인
      market = Market.objects.get(road_address=shop['roadAddress'])
      market_id = market.id
      # print(market.id)
      print("Market 있음")
    except Market.DoesNotExist:
      ## Market 데이터 저장
      market_data = {'market_name': shop['title'], 'latitude':shop['mapx'], 'longitude': shop['mapy'], 'road_address': shop['roadAddress']}
      serializer = MarketCreateSerializer(data=market_data)
      if serializer.is_valid():
        serializer.save()
        print("Market 저장 성공")
        market_id = Market.objects.get(road_address=shop['roadAddress']).id
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    try:
      # Item이 있는지 확인
      item = Item.objects.get(item_name=item_name)
      item_id = item.id
      # print(similar(list(bytes(item.item_name, 'utf-8')), list(bytes("페브리즈 상쾌한향 용기", 'utf-8'))))
      # print(similar(list(bytes(item.item_name, 'utf-8')), list(bytes("페브리즈 은은한향 용기", 'utf-8'))))
      item_data = {'item_name': item_name, 'item_search_count':(item.item_search_count+1)}
      serializer = ItemCreateSerializer(item, data=item_data)
      if serializer.is_valid():
        serializer.save()
        print("Item 수정 성공")
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Item.DoesNotExist:
      # Item 데이터 저장
      item_data = {'item_name': item_name, 'item_search_count':1}
      serializer = ItemCreateSerializer(data=item_data)
      if serializer.is_valid():
        serializer.save()
        print("Item 저장 성공")
        item_id = Item.objects.get(item_name=item_name).id
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
      market_items = MarketItems.objects.get(
        market_id=market_id,
        item_id=item_id
      )
      # print(market_items)
      market_items_data = {'market_id': market_id, 'item_id': item_id, 'item_price': item_price}
      serializer = MarketItemsCreateSerializer(market_items, data=market_items_data)
      if serializer.is_valid():
        serializer.save()
        print("MarketItems 수정 성공")
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
      # MarketItems 데이터 저장
      market_items_data = {'market_id': market_id, 'item_id': item_id, 'item_price': item_price}
      serializer = MarketItemsCreateSerializer(data=market_items_data)
      if serializer.is_valid():
        serializer.save()
        print("MarketItems 저장 성공")
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # naver_list_link = "https://msearch.shopping.naver.com/search/all?frm=NVSHMDL&origQuery="+encoded_item_name+"&pagingIndex=1&pagingSize=40&productSet=model&query="+encoded_item_name+"&sort=rel&viewType=lst"
    naver_list_link = "https://msearch.shopping.naver.com/search/all?query="+encoded_item_name+"&cat_id=&frm=NVSHATC"

    enuri_list_link = "https://m.enuri.com/m/search.jsp?keyword="+encoded_item_name

    danawa_list_link = "https://search.danawa.com/mobile/dsearch.php?keyword="+encoded_item_name

    final_result_dic = {
      'success': True, 
      'response': {
        'item': {
          'item_name': item_name
        },
        'shop': {
          'enuri': {
            'list': enuri_list_link
          },
          'danawa': {
            'list': danawa_list_link
          },
          'naver': {
            'list': naver_list_link
          },
        }
      },
      'error': None
    }

    return Response(final_result_dic)