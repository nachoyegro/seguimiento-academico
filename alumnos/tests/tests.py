from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Profile, Carrera, Alumno, AlumnoDeCarrera, PlanDeEstudio


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
        alumno1 = Alumno.objects.create(nombre='A', apellido='A', dni='A', email='A@a.com', legajo='2',
                                        sexo='M', telefono='', celular='',
                                        comentario='', observacion='')
        alumnodc1 = AlumnoDeCarrera.objects.create(alumno=alumno1,
                                                   carrera=tpi,
                                                   plan=p1,
                                                   promedio='8')
        alumno2 = Alumno.objects.create(nombre='B', apellido='B', dni='B', email='B@a.com', legajo='2',
                                        sexo='M', telefono='', celular='',
                                        comentario='', observacion='')
        alumnodc2 = AlumnoDeCarrera.objects.create(alumno=alumno2,
                                                   carrera=lds,
                                                   plan=p2,
                                                   promedio='8')
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

    def test_api_alumnos_sin_token(self):
        """
            Deberia darme status code 401, unauthorized
        """
        url = '/api/alumnos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_api_alumnos_con_token(self):
        """
            Deberia darme status code 200, Ok
        """
        self.acreditarse_con_token()
        url = '/api/alumnos/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api_alumnos_totales(self):
        """
            Deberia darme solo un alumno, ya que tengo asignada solo una carrera
        """
        self.acreditarse_con_token()
        url = '/api/alumnos/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)

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
        url = '/api/carreras/D/alumnos/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 0)

    def test_api_carreras(self):
        """
            Deberia darme solo la carrera que tengo asignada
        """
        self.acreditarse_con_token()
        url = '/api/carreras/'
        response = self.client.get(url)
        self.assertEquals(len(response.data), 1)
