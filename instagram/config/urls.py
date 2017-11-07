"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from config.views import to_post_list
from post.apis import PostList

urlpatterns = [
    # Django admin
    url(r'^admin/', admin.site.urls),
    url(r'^$', to_post_list),

    # Post application
    url(r'^post/', include('post.urls', namespace='post')),
    # Member application
    url(r'^member/', include('member.urls', namespace='member')),

    url(r'^api/post/$', PostList.as_view(), name='api-post'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
