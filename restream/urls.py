from django.urls import path
from . import views

app_name = 'restream'

urlpatterns = [
    path('restreamconfig/', views.RestreamConfigList.as_view(), name='restreamconfig_list'),
    path('restreamconfig/<int:pk>/', views.RestreamConfigDetail.as_view(), name='restreamconfig_detail'),
    path('restreamconfig/<int:pk>/delete', views.RestreamConfigDelete.as_view(), name='restreamconfig_delete'),
    path('restreamconfig/create', views.RestreamConfigCreate.as_view(), name='restreamconfig_create'),
]
