"""
URL configuration for advisor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from familyadvisor import views

urlpatterns = [
   
       path('admin/', admin.site.urls),
    # path('api/', include('advisor.urls')),
    #    path('test-mongodb-connection/', views.test_mongodb_connection, name='test-mongodb-connection'),
    # path('health/', views.health_check, name='health-check'),
    path('api/auth/', include('authentication.urls')),  # Include authentication URLs
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/', include('familyadvisor.urls')),
]
