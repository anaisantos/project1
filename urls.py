"""django_com_oracle_da_anav2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from uporto.django_com_oracle_da_anav2.core.views import check_status, redirects

# Endereços que não incluem particula do URL com o idioma.
urlpatterns = [
    path('', view=redirects, name='redirects'),  # Utilizar para redirecionar para página  default a partir dono url_base.
    path('i18n/', include('django.conf.urls.i18n')),  # Manter este endereço, essencial para a gestão do idioma.
    path('si_check_status', check_status, name='check_status'),  # Manter este endereço operacional, é para monitorização da aplicação.
    path(settings.BASE_API_URL, include('uporto.django_com_oracle_da_anav2.core.urls')),  # APIs
]
# Endereços que usam a particula do URL com o idioma.
urlpatterns += i18n_patterns(
    path('<str:uo>/', include('uporto.django_com_oracle_da_anav2.core.urls')),  # Páginas web com idioma e UO.
    path('admin/', admin.site.urls),
)
if settings.DEBUG:
    urlpatterns += i18n_patterns(
        path('__debug__/', include(debug_toolbar.urls)),
    )

# Static e media.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
