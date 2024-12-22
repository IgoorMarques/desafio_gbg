from rest_framework.viewsets import ModelViewSet

from cme_app.models import Processo
from cme_app.serializers import ProcessSerializer


class ProcessViewSet(ModelViewSet):
    queryset = Processo.objects.all()
    serializer_class = ProcessSerializer
