from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status
from search.models import Item

from search.serializers.serializers import ItemCreateSerializer

class ItemRankView(APIView):
    
  def get(self, request):
    items = Item.objects.all().order_by('-item_search_count')[:10]
    serializer = ItemCreateSerializer(items, many=True)

    final_result_dic = {
      'success': True, 
      'response': {
        'items': serializer.data
      },
      'error': None
    }

    return Response(final_result_dic)