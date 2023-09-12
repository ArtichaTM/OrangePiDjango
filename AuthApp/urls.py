from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('auth/login', views.login_view, name='post_login'),
    path('auth/signin', views.signin_view, name='post_signin'),
    path('auth/logout', views.logout_view, name='post_logout'),
    path('change_language/<str:target_lang>', views.change_language, name='change_language'),
    path('change_theme/<str:target_theme>', views.change_theme, name='change_theme'),
    path('auth/profile/<int:target_user>', views.profile_id, name='profile_id'),
    path('auth/profile/<str:target_user>', views.profile_username, name='profile_username')
]
