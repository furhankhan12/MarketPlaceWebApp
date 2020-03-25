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

    path('users/create_account', views.create_account, name='create_account'),
    path('users/login',views.login, name="login"),
    path('users/logout',views.logout,name='logout'),
    path('users/reset_password',views.reset_user_password,name='reset_password'),
    path('users/generate_token',views.generate_token,name='generate_token'),
    path('users/update_information',views.update_user_profile,name='update_user_profile'),
    path('users/get_user',views.get_user,name='get_user'),
    path('users/login', views.login, name='login'),
    path('users/logout', views.logout, name='logout'),
    # path('users', views.get_all_users, name='users_list'),
    path('users/<int:user_id>', views.get_user_with_id, name='get_user_id'),
    path('users/get_user_with_auth', views.get_user_with_auth, name='get_user_auth'),
    path('users/<int:user_id>/delete', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/update', views.update_user, name='update_user'),
    # path('users/new', views.new_user, name='new_user'),

    path('address/<int:address_id>', views.get_address, name='get_address'),
    path('address/<int:address_id>/update', views.update_address, name='update_address'),
    path('address/new', views.new_address, name='new_address'),

    path('profile/<int:profile_id>', views.get_profile, name='get_profile'),
    path('profile/<int:profile_id>/update', views.update_profile, name='update_profile'),
    path('profile/new/<int:user_id>', views.new_profile, name='new_profile'),
]
