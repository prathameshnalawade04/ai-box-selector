from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_order_and_find_box, name='box_selector'),
]