from django.urls import path  
from search.views import imageSearchAPIView, textSearchAPIView, blogReviewSearchAPIView, searchRankAPIView, searchMarketAPIView

urlpatterns = [  
  path('camera', imageSearchAPIView.ImageSearchView.as_view()),
  path('home', textSearchAPIView.TextSearchView.as_view()),
  path('item', textSearchAPIView.MapTextSearchView.as_view()),
  path('blog', blogReviewSearchAPIView.BlogReviewView.as_view()),
  path('blog/chatgpt', blogReviewSearchAPIView.BlogSummaryView.as_view()),
  path('rank', searchRankAPIView.ItemRankView.as_view()),
  path('market', searchMarketAPIView.SearchMarketView.as_view()),
]