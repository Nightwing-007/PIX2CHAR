from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import auth_views as custom_auth_views

urlpatterns = [
    # Main application views
    path('', views.home, name='home'),
    path('generate/', views.generate_ascii, name='generate_ascii'),
    path('result/<str:pk>/', views.view_result, name='view_result'),
    path('delete/<str:pk>/', views.delete_art, name='delete_art'),
    path('gallery/', views.gallery, name='gallery'),
    path('my-gallery/', views.my_gallery, name='my_gallery'),
    
    # Authentication views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', custom_auth_views.register, name='register'),
]