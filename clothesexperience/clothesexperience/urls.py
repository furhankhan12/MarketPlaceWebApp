"""clothesexperience URL Configuration

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
    path('listings', views.get_all_listings, name='listings'),
    path('listings/<int:listing_id>', views.get_listing, name='get_listing'),
    path('listings/new', views.new_listing, name='new_listing'),
    path('search/<slug:query>',views.get_searchResults,name='search'),
    path('users/signup',views.create_account, name='create_account'),
    path('users/login',views.login,name = 'login'),
    path('users/logout',views.logout,name='logout'),
    path('users/get_user_with_auth',views.get_user_with_auth,name='get_user_with_auth'),
]