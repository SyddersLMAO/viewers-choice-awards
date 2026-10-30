
from django.urls import path
from . import views

urlpatterns = [
    path('', views.nomination_categories, name='nominate'),
    path('success/', views.nomination_success, name='nomination_success'),
]
