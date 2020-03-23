from django.urls import path
from . import views

urlpatterns = [
    path('listings', views.get_all_listings, name='listings_list'),
    path('listings/<int:listing_id>', views.get_listing, name='get_listing'),
    path('listings/<int:listing_id>/delete', views.delete_listing, name='delete_listing'),
    path('listings/<int:listing_id>/update', views.update_listing, name='update_listing'),
    path('listings/new', views.new_listing, name='new_listing'),

    path('orders', views.get_all_orders, name='orders_list'),
    path('orders/<int:order_id>', views.get_order, name='get_order'),
    path('orders/<int:order_id>/delete', views.delete_order, name='delete_order'),
    path('orders/<int:order_id>/update', views.update_order, name='update_order'),
    path('orders/new', views.new_order, name='new_order'),

    # path('users/create_account', views.create_account, name='create_account'),
    # path('users/login', views.login, name='login'),
    # path('users/logout', views.logout, name='logout'),
    # path('users', views.get_all_users, name='users_list'),
    path('users/<int:user_id>', views.get_user, name='get_user'),
    path('users/<slug:user_name>',views.get_user_username,name='get_user_username'),
    # path('users/<int:user_id>/delete', views.delete_user, name='delete_user'),
    # path('users/<int:user_id>/update', views.update_user, name='update_user'),
    path('create_account/new', views.new_user, name='new_user'),
]
