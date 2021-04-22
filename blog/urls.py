from rest_framework.routers import DefaultRouter

from blog.api.blog_api import blog_ViewSet, blog_user_ViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('blog', blog_ViewSet, basename='blog')


urlpatterns = [
    path('', include(router.urls)),
    path('blog-user', blog_user_ViewSet.as_view())
    ]