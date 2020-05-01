from django.urls import path
from . import views

app_name = 'rtmp'

urlpatterns = [
    path('callback/srs', views.callback_srs, name='callback_srs'),
    path('streams/', views.StreamList.as_view(), name='stream_list'),
    path('streams/<int:pk>/', views.StreamDetail.as_view(), name='stream_detail'),
    path('streams/<int:pk>/change', views.StreamChange.as_view(), name='stream_change'),
    path('streams/<int:pk>/delete', views.StreamDelete.as_view(), name='stream_delete'),
    path('streams/create', views.StreamCreate.as_view(), name='stream_create'),
]
