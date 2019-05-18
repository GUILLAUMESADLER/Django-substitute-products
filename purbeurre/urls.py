"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_views.index, name='index'),
    path('search/results/', search_views.results, name='results'),
    path('search/product/<int:id>', search_views.product, name='product'),
    path('search/substitutes/<int:id>', search_views.substitutes, name='substitutes'),
    path('search/favorites/<int:id>', search_views.add_favorite, name='add_favorite'),
    path('search/favorites', search_views.favorites, name='favorites'),
    path('del_favorite/<int:id>', search_views.del_favorite, name='del_favorite'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('legales_notices/', search_views.legales_notices, name='legales_notices'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
