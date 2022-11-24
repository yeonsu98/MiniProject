from . import views
from django.urls import path

app_name = 'ml'
urlpatterns = [
    path('', views.list, name='list'),
    path('new', views.ml_model_create, name='create'),
]
