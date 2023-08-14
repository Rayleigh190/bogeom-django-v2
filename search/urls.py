from django.urls import path  
from search.views import imageSearchAPIView, textSearchAPIView

urlpatterns = [  
  path('camera', imageSearchAPIView.ImageSearchView.as_view()),
  path('home', textSearchAPIView.TextSearchView.as_view()),
]