"""uniondrug_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls


from article.views import ArticleViewset, CategoryViewset, TagViewset, AvatarViewset

# 注册默认路由
route = DefaultRouter()

route.register("article", ArticleViewset, basename="article")
route.register("category", CategoryViewset, basename="category")
route.register("tag", TagViewset, basename="tag")
route.register("avatar", AvatarViewset, basename="avatar")

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(route.urls)),
    url(r"^docs/", include_docs_urls("博客系统接口文档"))
]

# 注册媒体文件路由
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)