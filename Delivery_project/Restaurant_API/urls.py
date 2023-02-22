from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoriesView.as_view()),
    path('menuitem/', views.MenuitemsView.as_view()),
    path('groups/manager/users/', views.managers),
    
]