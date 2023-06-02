from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('qanda', views.qanda, name='qanda'),
    path('chat', views.chat, name='chat'),
    path('image', views.image, name='image')
]
