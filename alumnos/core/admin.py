from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from core.models import Postulantes, Inscripcion, Profile, Carrera, Alumno, Materia, MateriaEnPlan, MateriaCursada, PlanDeEstudio, AlumnoDeCarrera


class MateriaCursadaTabular(admin.TabularInline):
    model = MateriaCursada
    fields = ('fecha', 'materia', 'nota', 'resultado', 'forma_aprobacion')
    classes = ('grp-collapse grp-open',)
    raw_id_fields = ('materia', )
    extra = 0

class PostulantesInline(admin.StackedInline):
    model = Postulantes
    extra = 0

class PlanDeEstudioInline(admin.StackedInline):
    model = PlanDeEstudio
    extra = 0

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    inlines = [PlanDeEstudioInline, PostulantesInline]

class AlumnoDeCarreraStackedAdmin(admin.StackedInline):
    model = AlumnoDeCarrera
    extra = 0

class MateriaEnPlanTabularInline(admin.TabularInline):
    model = MateriaEnPlan

class InscripcionStackedAdmin(admin.StackedInline):
    model = Inscripcion
    extra = 0


class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('legajo', 'apellido', 'nombre', 'es_regular')
    search_fields = ('apellido', 'nombre', 'legajo')
    inlines = [AlumnoDeCarreraStackedAdmin,
               MateriaCursadaTabular, InscripcionStackedAdmin]


class MateriaAdmin(admin.ModelAdmin):
    list_display = ('materia', 'plan', 'carrera')

    def carrera(self, obj):
        return obj.plan.carrera

    carrera.short_description = 'carrera'
    carrera.admin_order_field = 'plan__carrera'

class PlanDeEstudioAdmin(admin.ModelAdmin):
    list_display = ('anio', 'carrera')
    inlines = [MateriaEnPlanTabularInline]

class ProfileInLine(admin.StackedInline):
    model = Profile
    filter_horizontal = ['carreras', ]

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInLine, ]

admin.site.site_url = 'http://127.0.0.1:3000/'
admin.site.site_header = "Seguimiento Academico Admin"
admin.site.site_title = "Seguimiento Academico"
admin.site.index_title = "Bienvenido al admin de seguimiento academico"
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(MateriaEnPlan, MateriaAdmin)
admin.site.register(PlanDeEstudio, PlanDeEstudioAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(MateriaCursada)
