from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lista/', views.lista, name='lista'),
    path('webhook/', views.webhook_mercadopago, name='webhook_mp'),
     path('resetar/', views.resetar_pix, name='resetar_pix'),
]