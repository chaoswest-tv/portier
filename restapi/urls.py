from django.urls import path, include
from rest_framework import routers

from .views import ApplicationViewSet, StreamViewSet, RestreamConfigViewSet


router = routers.DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'streams', StreamViewSet)
router.register(r'restreamconfigs', RestreamConfigViewSet)

app_name = 'restapi'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
