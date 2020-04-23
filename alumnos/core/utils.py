from core.models import *

def get_cantidad_graduados(carrera, anio):
    '''
        Retorna la cantidad de graduados de una carrera en un año determinado
    '''
    graduados = Graduado.objects.filter(alumno__carrera=carrera)
    return graduados.filter(fecha__year=anio).count()

def get_cantidad_ingresantes(carrera, anio):
    '''
        Retorna la cantidad de ingresantes de una carrera en un año determinado

        TODO: se podria hacer teniendo en cuenta MateriaCursada en vez de inscripcion. El problema es que materiacursada es pasado
    '''
    #inscriptos = Inscripcion.objects.filter(carrera=carrera)
    #return {"anio": anio, "cantidad": inscriptos.filter(fecha__year=anio).count()}
    
    #Filtro las materias de la carrera que son del ingreso
    materias_ingreso = [mep.materia for mep in MateriaEnPlan.objects.filter(plan__carrera=carrera, nucleo='I')]

    #Filtro todas las inscripciones de esa carrera y ese año de las materias anteriores
    inscripciones_ingreso = Inscripcion.objects.filter(carrera=carrera, fecha__year=anio, materia__in=materias_ingreso)

    #Devuelvo todos los alumnos distintos que se anotaron
    return len(inscripciones_ingreso.values_list('alumno_id').distinct())

def get_cantidad_cursantes(carrera, anio):
    '''
        Retorna la cantidad de cursantes de una carrera en un año determinado
        Se calcula con la cantidad de alumnos menos los ingresantes y graduados
    '''
    #Traigo a los alumnos de esa carrera TENIENDO EN CUENTA EL AÑO ACTUAL (Importante, puede cambiar)
    alumnos = AlumnoDeCarrera.objects.filter(carrera=carrera, fecha_inscripcion__year__lte=anio).count()
    #Traigo los graduados hasta el año anterior al actual
    graduados_hasta_anio = Graduado.objects.filter(alumno__carrera=carrera, fecha__year__lt=anio).count()
    #La cantidad de cursantes es la cantidad total de alumnos contando el año actual, menos los ingresantes de este año, menos los graduados totales
    cursantes = alumnos - get_cantidad_ingresantes(carrera, anio) - graduados_hasta_anio
    return cursantes
    
def get_cantidad_postulantes(carrera, anio):
    '''
        Retorna la cantidad de postulantes de una carrera en un año determinado
    '''
    postulantes = 0
    for ps in Postulantes.objects.filter(carrera=carrera, fecha__year=anio):
        postulantes += ps.cantidad
    return postulantes
    

