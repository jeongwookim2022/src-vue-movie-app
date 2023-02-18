from django.urls import path
from . import views
urlpatterns = [
    ############# Function based ##############
    # path("menu-items/", views.menu_items),
    # path("menu-items/<int:id>", views.single_item),
    
    ############# Class based ###################
    path('menu-items/', views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>', views.MenuItemsViewSet.as_view({'get':'retrieve'})),
]