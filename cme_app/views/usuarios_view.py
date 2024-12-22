from rest_framework.viewsets import ModelViewSet

from cme_app.models import Usuario
from cme_app.serializers import UserSerializer


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
