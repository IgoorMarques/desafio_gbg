from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Rota do admin
    path('api/', include('cme_app.urls')),  # Inclui as rotas do app cme_app
]
