from django.contrib import admin
from core.models import Alumno, Materia, MateriaCursada, PlanDeEstudio, Comision, AlumnoDeCarrera

class MateriaCursadaTabular(admin.TabularInline):
    model = MateriaCursada
    fields = ('comision', 'nota')
    classes = ('grp-collapse grp-open',)
    raw_id_fields = ('comision', )

class AlumnoDeCarreraStackedAdmin(admin.StackedInline):
    model = AlumnoDeCarrera
    extra = 0

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre','legajo', 'es_regular')
    search_fields = ('apellido', 'nombre', 'legajo')
    inlines = [AlumnoDeCarreraStackedAdmin]

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(PlanDeEstudio)
admin.site.register(Comision)
