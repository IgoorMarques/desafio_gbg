from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from cme_app.views import UsuarioViewSet, MaterialViewSet, ProcessViewSet
from cme_app.views.relatorios_view import gerar_relatorio_pdf, gerar_relatorio_xlsx

# Configuração do router para as views
router = DefaultRouter()
router.register('users', UsuarioViewSet)
router.register('materials', MaterialViewSet)
router.register('processes', ProcessViewSet)

urlpatterns = [
    # Endpoints REST
    path('rest/', include(router.urls)),
    path('api/relatorios/pdf/', gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('api/relatorios/xlsx/', gerar_relatorio_xlsx, name='gerar_relatorio_xlsx'),
    # Documentação da API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
