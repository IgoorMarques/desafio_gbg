from reportlab.pdfgen import canvas
from django.http import HttpResponse

from cme_app.models import Processo


def gerar_relatorio_pdf(request, serial=None):
    # Obter dados filtrados
    if serial:
        processos = Processo.objects.filter(serial_material__serial=serial)
    else:
        processos = Processo.objects.all()

    # Configurar resposta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_rastreabilidade.pdf"'

    # Criar PDF
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Relatório de Rastreabilidade")
    y = 750
    for processo in processos:
        p.drawString(50, y,
                     f"Serial: {processo.serial_material.serial} | Etapa: {processo.etapa} | Status: {processo.status} | Usuário: {processo.usuario_responsavel.username} | Data: {processo.data_hora}")
        y -= 20

    p.showPage()
    p.save()
    return response
