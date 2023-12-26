from django.contrib import admin
from django.db import router
from rest_framework import routers
from django.urls import path, include
from shop.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'prod', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("shop.urls")),
    path('accounts/', include("accounts.urls")),
    path('api2/', include(router.urls)),

]
