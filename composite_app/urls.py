from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path as url

urlpatterns = [
    path('', views.home, name="home"),
    url('predictImage',views.predictImage, name='predictImage')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)