from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Profile, Carrera, Alumno, AlumnoDeCarrera, PlanDeEstudio, Materia, MateriaEnPlan, MateriaCursada, Inscripcion


class ApiTestCase(APITestCase):

    def setUp(self):
        tpi = Carrera.objects.create(nombre='TPI - Tecnicatura Universitaria en Programación Informática',
                                     codigo='P')
        lds = Carrera.objects.create(nombre='LDS - Licenciatura en Informática',
                                     codigo='W')
        p1 = PlanDeEstudio.objects.create(
            nombre='2015', carrera=tpi, anio=2015)
        p2 = PlanDeEstudio.objects.create(
            nombre='2015', carrera=lds, anio=2015)
        alumno1 = Alumno.objects.create(nombre='A', apellido='A', dni='A', email='A@a.com', legajo='21872',
                                        sexo='M', telefono='', celular='',
                                        comentario='', observacion='')
        _ = AlumnoDeCarrera.objects.create(alumno=alumno1,
                                           carrera=tpi,
                                           plan=p1,
                                           promedio='8')
        alumno2 = Alumno.objects.create(nombre='B', apellido='B', dni='B', email='B@a.com', legajo='2888',
                                        sexo='M', telefono='', celular='',
                                        comentario='', observacion='')
        _ = AlumnoDeCarrera.objects.create(alumno=alumno2,
                                           carrera=lds,
                                           plan=p2,
                                           promedio='8')

        materia_tpi = Materia.objects.create(siglas="tpi", codigo="01037")
        materia_en_plan_tpi = MateriaEnPlan.objects.create(
            materia=materia_tpi, codigo="01037", plan=p1)
        _ = MateriaCursada.objects.create(
            alumno=alumno1, materia=materia_en_plan_tpi, carrera=tpi, nota="8")

        materia_lds = Materia.objects.create(siglas="lds", codigo="01046")
        materia_en_plan_lds = MateriaEnPlan.objects.create(
            materia=materia_lds, codigo="01046", plan=p2)
        _ = MateriaCursada.objects.create(
            alumno=alumno2, materia=materia_en_plan_lds, carrera=lds, nota="9")
        _ = MateriaCursada.objects.create(
            alumno=alumno1, materia=materia_en_plan_lds, carrera=lds, nota="7")

        _ = Inscripcion.objects.create(
            carrera=tpi, alumno=alumno1, materia=materia_tpi)
        _ = Inscripcion.objects.create(
            carrera=lds, alumno=alumno2, materia=materia_lds)

        # Agrego una inscripcion en dos carreras asi me muestra solo una, ya que en la otra no tengo permiso
        _ = Inscripcion.objects.create(
            carrera=lds, alumno=alumno1, materia=materia_lds)

        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = User.objects.create_user(**self.credentials)
        profile = Profile.objects.create(user=self.user)
        profile.carreras.add(tpi)
        profile.save()

    def pedir_token(self):
        url = reverse('token')
        return self.client.post(url, self.credentials, follow=True)

    def acreditarse_con_token(self):
        response_token = self.pedir_token()
        token = response_token.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_jwt_token_200(self):
        """
            Pido el token con las credenciales, y deberia darme status code 200
        """
        response = self.pedir_token()
        self.assertEqual(response.status_code, 200)

    def test_jwt_token_access(self):
        """
            Pido el token con las credenciales, y deberia darme un token
        """
        response = self.pedir_token()
        self.assertTrue('access' in response.data.keys())

    ######## Alumnos de carrera ##################

    def test_api_alumnos_de_carrera_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/carreras/P/alumnos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_alumnos_de_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/carreras/P/alumnos/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_alumnos_de_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/carreras/W/alumnos/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ######### Carreras ############

    def test_api_carreras(self):
        """
            Deberia retornar todas las carreras disponibles
        """
        self.acreditarse_con_token()
        url = '/api/carreras/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_carreras_sin_token(self):
        """
            Deberia retornar todas las carreras disponibles
        """
        url = '/api/carreras/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    ########## Materias cursadas de carrera #############
    def test_api_materias_de_carrera_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/carreras/P/materiascursadas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_materias_de_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/carreras/P/materiascursadas/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_materias_de_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/carreras/W/materiascursadas/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ########## Inscripciones de alumno #############
    def test_api_inscripciones_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/alumno/21872/inscripciones/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_inscripciones_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/alumno/21872/inscripciones/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_inscripciones_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/alumno/2888/inscripciones/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ########## Materias cursadas de alumno #############
    def test_api_cursadas_alumno_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/alumno/21872/cursadas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_cursadas_alumno_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/alumno/21872/cursadas/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_cursadas_alumno_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/alumno/2888/cursadas/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ########## Materias cursadas de alumno #############
    def test_api_cursadas_alumno_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/alumno/21872/cursadas/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_cursadas_alumno_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/alumno/21872/cursadas/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_cursadas_alumno_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/alumno/2888/cursadas/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ########## Materias de un plan #############
    def test_api_materias_plan_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/carreras/P/planes/2015/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_materias_plan_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/carreras/P/planes/2015/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_materias_plan_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/carreras/W/planes/2015/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ########## Planes de una carrera #############
    def test_api_planes_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/carreras/P/planes/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_planes_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/carreras/P/planes/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_planes_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/carreras/W/planes/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    ########## Alumnos de una materia #############
    def test_api_alumnos_materia_sin_token(self):
        """
            Deberia retornar error 401 unauthorized
        """
        url = '/api/materia/01037/alumnos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_alumnos_materia_carrera_asignada(self):
        """
            Deberia darme una lista con un elemento
        """
        self.acreditarse_con_token()
        url = '/api/materia/01037/alumnos/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

    def test_api_alumnos_materia_carrera_no_asignada(self):
        """
            Deberia darme una lista vacia
        """
        self.acreditarse_con_token()
        url = '/api/materia/01046/alumnos/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)
