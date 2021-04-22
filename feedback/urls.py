from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feedback.api.feedback_api import FeedBackViewSet

router = DefaultRouter()
router.register('feedback', FeedBackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]