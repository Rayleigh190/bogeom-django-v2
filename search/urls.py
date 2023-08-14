from django.urls import path  
from search.views import imageSearchAPIView

urlpatterns = [  
  path('camera', imageSearchAPIView.ImageSearchView.as_view()),
]