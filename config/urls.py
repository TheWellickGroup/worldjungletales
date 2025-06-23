"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import RedirectView

from common.sitemap import StaticViewSitemap, TopicSiteMap, WorldJungleTalesSiteMap
from config import settings

sitemaps = {
    "articles": WorldJungleTalesSiteMap,
    "topics": TopicSiteMap,
    "static": StaticViewSitemap,
}

handler404 = "worldjungletales.views.error_404"
handler500 = "worldjungletales.views.error_500"

urlpatterns = [
    path("", include("worldjungletales.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "favicon.ico",
        RedirectView.as_view(
            url="https://rturvxlqpsxpkqobiybe.supabase.co/storage/v1/object/public/media/assets/favicon/favicon-16x16.png"
        ),
    ),
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
