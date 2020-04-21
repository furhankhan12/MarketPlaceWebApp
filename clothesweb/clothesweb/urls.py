"""clothesweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clothes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'), 

    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('listing/<int:listing_id>/update', views.update_listing, name='update_listing'),
    path('listing/<int:listing_id>/delete', views.delete_listing, name='delete_listing'),
    path('listing/new', views.new_listing, name='new_listing'),

    path('search/results/',views.search_results, name='search'),
    path('search/results/popular/<slug:query>',views.get_most_popular, name='search_popular'),

    path('users/signup/',views.create_account, name='create_account'),
    path('users/login',views.login,name='login'),
    path('users/logout',views.logout,name='logout'),
    path('users/reset_password_email',views.reset_password_email,name="reset_password_email"),
    path('users/reset_password/<slug:token>',views.reset_password,name='reset_password'),
    path('users/update_information',views.update_user_profile,name='update_user_profile'),
    path('users/profile',views.user_profile,name='user_profile'),

]
