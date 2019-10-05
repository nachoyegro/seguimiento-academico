from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class AlumnosTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agrego las carreras al payload
        if user.profile:
            token['carreras'] = [carrera.pk for carrera in user.profile.carreras.all()]
        return token

class AlumnosTokenObtainPairView(TokenObtainPairView):
    serializer_class = AlumnosTokenObtainPairSerializer
