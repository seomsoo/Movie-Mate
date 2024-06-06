from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.profile,),
    path('follow/<str:username>/', views.follow),
    path('isfollow/<str:username>/', views.is_followed),
    path('user/<str:username>/', views.user),
    path('get_user/', views.get_user)
]
