"""alumnos URL Configuration

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
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from core.views import ImportarMateriasCursadasView, ImportarDatosAlumnosView, ImportarInscripcionesView, ImportarRequisitosView, ImportarPlanesView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Nucleo Academico API')

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls, name='admin'),
    path(r'admin/core/importar_materias_cursadas/',
         ImportarMateriasCursadasView.as_view(), name='importador_materias_cursadas'),
    path(r'admin/core/importar_alumnos/',
         ImportarDatosAlumnosView.as_view(), name='importador_alumnos'),
    path(r'admin/core/importar_inscripciones/',
         ImportarInscripcionesView.as_view(), name='importador_inscripciones'),
    path(r'admin/core/importar_requisitos/',
         ImportarRequisitosView.as_view(), name='importador_requisitos'),
    path(r'admin/core/importar_planes/',
         ImportarPlanesView.as_view(), name='importador_planes'),
    path('api/', include('core.urls')),
    path('docs/', schema_view),

    path('', RedirectView.as_view(url='admin', permanent=False), name='index')
    #url(r'^graphql', GraphQLView.as_view(graphiql=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
