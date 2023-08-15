from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import urllib.parse
from search.models import Item
from search.serializers.serializers import MapItemSerializer

class TextSearchView(APIView):
    
  def get(self, request):
    item_name = request.GET['search']
    encoded_item_name = urllib.parse.quote(item_name)

    naver_list_link = "https://msearch.shopping.naver.com/search/all?frm=NVSHMDL&origQuery="+encoded_item_name+"&pagingIndex=1&pagingSize=40&productSet=model&query="+encoded_item_name+"&sort=rel&viewType=lst"

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
  

class MapTextSearchView(APIView):
    
  def get(self, request):
    item_name = request.GET['search']
    
    items = Item.objects.filter(item_name__contains=item_name)
    serializer = MapItemSerializer(items, many=True)

    final_result_dic = {
      'success': True, 
      'response': {
        'items': serializer.data
      },
      'error': None
    }

    return Response(final_result_dic)