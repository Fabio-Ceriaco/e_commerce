from django.urls import path
from .views import *


app_name = 'store'
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('user_profile/', user_profile, name='user_profile'),
    path('update_info/', update_info, name='update_info'),
    path('update_password/', update_password, name='update_password'),
    path('products/<str:signed_id>/', product, name='product'),
    path('category/<str:category>/', category, name='category'),
    path('category_summary/', category_summary, name='category_summary'),
    path('search_product/', search_product, name='search_product'),
    
]
