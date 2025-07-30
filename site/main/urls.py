# Ссылки на странички. Каждую новую страницу добавлять сюда
from django.contrib import admin
from django.urls import path, include
from  . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('',views.index),
    path('index/', views.index, name='index'),
    path('registr/', views.registr, name='registr'),
    path('success/', views.success, name='success'),
    path('success1/', views.success, name='success1'),
    path('media/', views.media, name='media_view'),
    path('welcome-message/', views.WelcomeMessageView.as_view()),
    path('fan/on/', views.turn_fan_on, name='turn_fan_on'),
    path('water/on/', views.turn_water_on, name='turn_water_on'),
    path('download_csv/', views.download_csv, name='download_csv'),
    # path('report/', views.report_page, name='report_page'),
    path('', include(router.urls))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)