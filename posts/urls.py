from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostIndex.as_view(), name='index'),
    path('categories/<str:categoria>', views.PostCategories.as_view(), name='categories'),
    path('search/', views.PostSearch.as_view(), name='search'),
    path('post/<int:pk>', views.PostDetails.as_view(), name='details'),
]