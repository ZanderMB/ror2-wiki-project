from django.urls import path
from ROR2_Wiki import views

urlpatterns = [
    path('', views.home, name='home'),

    path('survivors/', views.SurvivorListView.as_view(), name='survivor-list'),
    path('survivor/<str:pk>/', views.SurvivorDetailView.as_view(), name='survivor-detail'),

    path('monsters/', views.MonsterListView.as_view(), name='monster-list'),
    path('monster/<str:pk>/', views.MonsterDetailView.as_view(), name='monster-detail'),

    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('item/<str:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
]
