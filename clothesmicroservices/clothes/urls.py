from django.urls import path
from . import views

urlpatterns = [
    path('listings/', views.get_all_listings, name='listings_list'),
    path('orders/', views.get_all_orders, name='orders_list'),
    path('users/', views.get_all_users, name='users_list'),

    # get 
    path('listings/<int:listing_id>', views.get_listing, name='get_listing'),
    path('listings/<int:listing_id>/delete', views.delete_listing, name='delete_listing'),
    path('listings/<int:listing_id>/update', views.update_listing, name='update_listing'),
    path('listings/new', views.new_listing, name='new_listing'),
    # path('listings/<int:listing_id>/update', views.update_listing, name='update_listing'),
    # path('orders/', views.get_all_orders, name='orders_list'),
    # path('users/', views.get_all_users, name='users_list'),


]
