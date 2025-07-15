from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'app'

urlpatterns = [
    path('app/', include(router.urls)),
]