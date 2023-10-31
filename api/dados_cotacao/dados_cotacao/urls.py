from django.contrib import admin
from django.urls import path ,include,re_path
from app.views import *
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cotacao/<str:data_solicitada>/', views.Cotacao, name='cotacao')
]
