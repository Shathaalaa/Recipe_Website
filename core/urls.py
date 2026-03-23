from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about')
    #path('index/', views.index, name='index')
]