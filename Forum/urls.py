from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('new_post', views.new_post, name='new_post'),
    # path('new_post/add_post', views.add_post, name='add_post'),
    # path('view/<int:post_id>', views.view_post, name='view_post')
]
