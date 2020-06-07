from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from core.models import Postulantes, Inscripcion, Profile, Carrera, Alumno, Materia, MateriaEnPlan, MateriaCursada, PlanDeEstudio, AlumnoDeCarrera


class MateriaCursadaTabular(admin.TabularInline):
    model = MateriaCursada
    fields = ('fecha','materia', 'carrera','nota', 'resultado', 'forma_aprobacion')
    classes = ('grp-collapse grp-open',)
    raw_id_fields = ('materia', 'carrera')
    readonly_fields = ('carrera', )
    extra = 0

    # Filtro las carreras del usuario
    def get_queryset(self, request):
        qs = super(MateriaCursadaTabular, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(carrera__in=request.user.profile.carreras.all())
        else:
            return qs.none()

class PostulantesInline(admin.StackedInline):
    model = Postulantes
    extra = 0

class PlanDeEstudioInline(admin.StackedInline):
    model = PlanDeEstudio
    extra = 0

class CarreraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    inlines = [PlanDeEstudioInline, PostulantesInline]

    # Filtro las carreras del usuario
    def get_queryset(self, request):
        qs = super(CarreraAdmin, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(pk__in=request.user.profile.carreras.all().values('pk'))
        else:
            return qs.none()

class AlumnoDeCarreraStackedAdmin(admin.StackedInline):
    model = AlumnoDeCarrera
    verbose_name = "Carrera del Alumno"
    verbose_name_plural = "Carreras del Alumno"
    extra = 0

    # Filtro las carreras del usuario
    def get_queryset(self, request):
        qs = super(AlumnoDeCarreraStackedAdmin, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(carrera__in=request.user.profile.carreras.all())
        else:
            return qs.none()

class MateriaEnPlanTabularInline(admin.TabularInline):
    model = MateriaEnPlan

    # Filtro las carreras del usuario
    def get_queryset(self, request):
        qs = super(MateriaEnPlanTabularInline, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(plan__carrera__in=request.user.profile.carreras.all())
        else:
            return qs.none()

class InscripcionStackedAdmin(admin.StackedInline):
    model = Inscripcion
    verbose_name = "Inscripción"
    verbose_name_plural = "Inscripciones"
    extra = 0

    # Filtro las carreras del usuario
    def get_queryset(self, request):
        qs = super(InscripcionStackedAdmin, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(carrera__in=request.user.profile.carreras.all())
        else:
            return qs.none()

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('legajo', 'apellido', 'nombre', 'es_regular')
    search_fields = ('apellido', 'nombre', 'legajo')
    inlines = [AlumnoDeCarreraStackedAdmin,
               MateriaCursadaTabular, InscripcionStackedAdmin]

    # Filtro los alumnos en base a la carrera del usuario
    def get_queryset(self, request):
        qs = super(AlumnoAdmin, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(pk__in=AlumnoDeCarrera.objects.filter(carrera__in=request.user.profile.carreras.all()).values_list('pk'))
        else:
            return qs.none()

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('materia', 'plan', 'carrera')
    search_fields = ('materia__nombre', 'plan__nombre', 'plan__carrera__nombre')

    def carrera(self, obj):
        return obj.plan.carrera

    carrera.short_description = 'carrera'
    carrera.admin_order_field = 'plan__carrera'

    # Filtro los alumnos en base a la carrera del usuario
    def get_queryset(self, request):
        qs = super(MateriaAdmin, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(plan__carrera__in=request.user.profile.carreras.all())
        else:
            return qs.none()

class PlanDeEstudioAdmin(admin.ModelAdmin):
    list_display = ('anio', 'carrera')
    inlines = [MateriaEnPlanTabularInline]

    # Filtro los alumnos en base a la carrera del usuario
    def get_queryset(self, request):
        qs = super(PlanDeEstudioAdmin, self).get_queryset(request)
        if request.user.profile:
            # Filtro los alumnos de las carreras del usuario
            return qs.filter(carrera__in=request.user.profile.carreras.all())
        else:
            return qs.none()

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
