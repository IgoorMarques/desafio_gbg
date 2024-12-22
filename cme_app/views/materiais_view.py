from rest_framework.viewsets import ModelViewSet

from cme_app.models import Material
from cme_app.serializers import MaterialSerializer


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
