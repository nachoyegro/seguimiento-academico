from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class AlumnosTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agrego las carreras al payload
        if user.profile:
            token['carreras'] = [carrera.codigo for carrera in user.profile.carreras.all()]
            token['username'] = user.username
        return token

class AlumnosTokenObtainPairView(TokenObtainPairView):
    serializer_class = AlumnosTokenObtainPairSerializer
