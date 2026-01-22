"""
URL configuration for backend project.

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
from django.urls import include, path
from . import views
from pliope.models import Person
from django.conf.urls.static import static
from django.conf import settings
from Games.models import Game




person_list = Person.objects.all()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('pliope/', include('pliope.urls')),
    path("ejemplopersona", views.homepage),
    path("__reload__/", include("django_browser_reload.urls")),
    path('users/', include('Users.urls')),
    path('productos/', include('Productos.urls')),
    path('Games/', include('Games.urls')),
    path('Api/', include('Api.urls')),
    
    
]
urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)