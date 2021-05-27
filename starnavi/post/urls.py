from django.urls import path
from .dateconverter import YearMonthDayConverter
from .views import (
    PostListView, 
    PostLikesListView, 
    PostLikesListViewByDate, 
    PostDetailView
)

urlpatterns = [
    path('', PostListView.as_view()),
    path('likes/', PostLikesListView.as_view()),
    path('<int:post>/', PostDetailView.as_view()),
    path('<yyyy-mm-dd:from>/<yyyy-mm-dd:to>', PostLikesListViewByDate.as_view()),
]
