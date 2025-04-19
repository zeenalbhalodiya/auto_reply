from django.urls import path
from .views import AutoReplyAPI

urlpatterns = [
    path('auto-reply/', AutoReplyAPI.as_view()),
]
