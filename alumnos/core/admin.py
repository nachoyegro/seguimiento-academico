from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from core.models import Profile, Carrera, Alumno, Materia, MateriaEnPlan, MateriaCursada, PlanDeEstudio, Comision, AlumnoDeCarrera

class MateriaCursadaTabular(admin.TabularInline):
    model = MateriaCursada
    fields = ('materia', 'nota')
    classes = ('grp-collapse grp-open',)
    raw_id_fields = ('materia', )
    extra = 0

class MateriaEnPlanTabular(admin.TabularInline):
    model = MateriaEnPlan
    extra = 0

class AlumnoDeCarreraStackedAdmin(admin.StackedInline):
    model = AlumnoDeCarrera
    extra = 0

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre','legajo', 'es_regular')
    search_fields = ('apellido', 'nombre', 'legajo')
    inlines = [AlumnoDeCarreraStackedAdmin, MateriaCursadaTabular]

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')
    inlines = [MateriaEnPlanTabular]

class ProfileInLine(admin.StackedInline):
    model = Profile
    filter_horizontal = ['carreras',]

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInLine,]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(PlanDeEstudio)
admin.site.register(Comision)
admin.site.register(Carrera)
admin.site.register(MateriaCursada)
