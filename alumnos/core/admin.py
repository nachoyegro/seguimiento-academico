from django.contrib import admin
from core.models import Alumno, Materia, MateriaCursada, PlanDeEstudio

def apellido(obj):
    return obj.datos_personales.apellido
apellido.short_description = 'Apellido'

def nombre(obj):
    return obj.datos_personales.nombre
nombre.short_description = 'Nombre'

class MateriaCursadaTabular(admin.TabularInline):
    model = MateriaCursada
    fields = ('materia', 'nota')
    classes = ('grp-collapse grp-open',)

class AlumnoAdmin(admin.ModelAdmin):
    list_display = (apellido, nombre,'legajo', 'es_regular')
    search_fields = ('datos_personales__apellido', 'datos_personales__nombre', 'legajo')
    inlines = [MateriaCursadaTabular, ]

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas', 'codigo')

class PlanDeEstudioAdmin(admin.ModelAdmin):
    readonly_fields = ('materias', )

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(PlanDeEstudio, PlanDeEstudioAdmin)
