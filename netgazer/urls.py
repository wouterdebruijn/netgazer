"""
URL configuration for netgazer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from netgazer import viewsets
from .views.DeviceViews import device_map
from . import models
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from .views.discovery_view import AsyncView

router = DefaultRouter()
router.register(r'devices', viewsets.DeviceViewSet)
router.register(r'interfaces', viewsets.InterfaceViewSet)
router.register(r'neighbors', viewsets.NeighborViewSet)

admin.site.register(models.Device)
admin.site.register(models.Interface)
admin.site.register(models.Neighbor)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('map/', device_map),
    path('discovery/', csrf_exempt(AsyncView.as_view())),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
