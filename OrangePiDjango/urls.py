from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('AuthApp.urls', 'AuthApp'), namespace='AuthApp')),
    path('posts/', include(('Posts.urls', 'Posts'), namespace='Posts')),
    path('forum/', include(('Forum.urls', 'Forum'), namespace='Forum'))
]
