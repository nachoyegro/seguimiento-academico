from django.contrib import admin
from core.models import Alumno, Materia, MateriaCursada, PlanDeEstudio, Comision

def apellido(obj):
    return obj.datos_personales.apellido
apellido.short_description = 'Apellido'

def nombre(obj):
    return obj.datos_personales.nombre
nombre.short_description = 'Nombre'

class MateriaCursadaTabular(admin.TabularInline):
    model = MateriaCursada
    fields = ('comision', 'nota')
    classes = ('grp-collapse grp-open',)
    raw_id_fields = ('comision', )

class AlumnoAdmin(admin.ModelAdmin):
    list_display = (apellido, nombre,'legajo', 'es_regular')
    search_fields = ('datos_personales__apellido', 'datos_personales__nombre', 'legajo')

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(PlanDeEstudio)
admin.site.register(Comision)
