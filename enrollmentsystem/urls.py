"""enrollmentsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from authority import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('', include('pages.urls')),
    #path('records/', include('records.urls')),
    #path('accounts/', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path(
        'accounts/login/',
        LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path("accounts/register", views.register_request, name="register"),
    path("accounts/myaccount/",
         views.user_profile, name="myaccount"),
    path("accounts/application", views.my_application, name="application"),
    path('enrollment/', include('records.urls', namespace='records')),
    path(
        'accounts/logout/',
        LogoutView.as_view(),
        name='logout',
    ),
    path("accounts/downloadform", views.download_form, name="download-form"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
