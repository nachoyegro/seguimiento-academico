from django.test import TestCase
from core.materia_cursada_creator import MateriaCursadaCreator
from core.models import MateriaCursada, Materia, MateriaEnPlan, PlanDeEstudio, AlumnoDeCarrera, Alumno, Carrera
from datetime import datetime

class MateriaCursadaCreatorTest(TestCase):

    def setUp(self):
        self.mc_creator = MateriaCursadaCreator()
        Carrera.objects.create(codigo='W') #MateriaCursadaCreator asume que ya existe la carrera
        self.data = {'legajo': '21872',
                    'dni': '35905769',
                    'codigo_carrera': 'W',
                    'codigo_materia': '1234',
                    'nombre_materia': 'Materia Falsa',
                    'fecha': datetime.strptime('21/06/2013', '%d/%m/%Y'),
                    'resultado': 'P',
                    'nota': '9',
                    'forma_aprobacion': 'Promocion',
                    'creditos': 12,
                    'acta_promocion': '',
                    'acta_examen': '',
                    'plan': 2012}
        self.mc_creator.create(**self.data)

    def test_alumno_creado(self):    
        alumno = Alumno.objects.all()[0]
        self.assertEquals(alumno.dni, '35905769')
        self.assertEquals(alumno.legajo, '21872')

    def test_materia_cursada_creada(self):
        cantidad_materias_cursadas = MateriaCursada.objects.all().count()
        self.assertEquals(cantidad_materias_cursadas, 1)

    def test_materia_creada(self):
        materia = Materia.objects.all()[0]
        self.assertEquals(materia.codigo, '1234')
        self.assertEquals(materia.nombre, 'Materia Falsa')

    def test_plan_creado(self):
        plan = PlanDeEstudio.objects.all()[0]
        self.assertEquals(plan.anio, 2012)
        self.assertEquals(plan.nombre, '2012')

    def test_alumno_de_carrera_creado(self):
        cant_alumnos = AlumnoDeCarrera.objects.all().count()
        self.assertEquals(cant_alumnos, 1)

    def test_alumno_de_carrera_correcta(self):
        alumno_de_carrera = AlumnoDeCarrera.objects.all()[0]
        self.assertEquals(alumno_de_carrera.carrera.codigo, 'W')

    def test_alumno_de_carrera_con_plan(self):
        alumno_de_carrera = AlumnoDeCarrera.objects.all()[0]
        self.assertEquals(alumno_de_carrera.plan.anio, 2012)

    def test_alumno_de_carrera_actualiza_plan_nuevo(self):
        """
            Como el plan de la nueva materia a guardar es mas actual
            Se actualiza el plan actual del alumno
        """
        self.data['plan'] = 2015
        self.mc_creator.create(**self.data)
        alumno_de_carrera = AlumnoDeCarrera.objects.all()[0]
        self.assertEquals(alumno_de_carrera.plan.anio, 2015)

    def test_alumno_de_carrera_no_actualiza_plan(self):
        """
            Como el plan de la nueva materia a guardar es mas antiguo
            No se actualiza el plan actual del alumno
        """
        self.data['plan'] = 2010
        self.mc_creator.create(**self.data)
        alumno_de_carrera = AlumnoDeCarrera.objects.all()[0]
        self.assertEquals(alumno_de_carrera.plan.anio, 2012)


    def test_nota_aprobada_cuando_no_hay_nota_y_el_resultado_es_A(self):
        self.data['nota'] = ''
        self.data['resultado'] = 'A'
        self.mc_creator.create(**self.data)
        #Traigo la nueva materia creada
        materia_cursada = MateriaCursada.objects.all()[1]
        self.assertEquals(materia_cursada.nota, 'A')

    def test_nota_no_aprobada_cuando_el_resultado_no_es_A(self):
        self.data['nota'] = ''
        self.data['resultado'] = 'U'
        self.mc_creator.create(**self.data)
        #Traigo la nueva materia creada
        materia_cursada = MateriaCursada.objects.all()[1]
        self.assertEquals(materia_cursada.nota, '')





