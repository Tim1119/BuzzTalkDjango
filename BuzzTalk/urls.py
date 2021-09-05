from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('posts.urls',namespace='posts')),
    path('comment/',include('Comment.urls',namespace='Comment')),
    path('profile/',include('profiles.urls',namespace='profiles')),
    path('users/', include('django.contrib.auth.urls')),
    path('users/',include('users.urls')),
]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

