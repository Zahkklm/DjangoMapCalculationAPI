from django.contrib import admin
from django.urls import path
from api.views import RouteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('route/', RouteView.as_view(), name='route'),
]