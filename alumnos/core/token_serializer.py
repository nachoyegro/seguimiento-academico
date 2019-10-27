from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class AlumnosTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agrego las carreras al payload
        try:
            token['carreras'] = [
                carrera.codigo for carrera in user.profile.carreras.all()]
            token['username'] = user.username
        except:
            token['carreras'] = []
            token['username'] = ''
        return token


class AlumnosTokenObtainPairView(TokenObtainPairView):
    serializer_class = AlumnosTokenObtainPairSerializer
