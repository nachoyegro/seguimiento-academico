from django.urls import path
from .views import ListPersonasView, ListAlumnosView


urlpatterns = [
    path('personas/', ListPersonasView.as_view(), name="personas-all"),
    path('alumnos/', ListAlumnosView.as_view(), name="alumnos-all")
]
