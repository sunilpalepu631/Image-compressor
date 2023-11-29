
from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter
# from rest_framework.routers import DefaultRouter

# router = SimpleRouter()
# router.register(r'image', postImage, basename='images')

urlpatterns = [
    path('<int:pk>/', postImage.as_view()),
    path('', postImage.as_view()),

]

# urlpatterns = router.urls

