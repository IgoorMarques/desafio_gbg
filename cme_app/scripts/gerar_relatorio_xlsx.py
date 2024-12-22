import openpyxl
from django.http import HttpResponse

from cme_app.models import Processo


def gerar_relatorio_xlsx(request, serial=None):
    # Obter dados filtrados
    if serial:
        processos = Processo.objects.filter(serial_material__serial=serial)
    else:
        processos = Processo.objects.all()

    # Criar arquivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rastreabilidade"
    ws.append(["Serial", "Etapa", "Status", "Usuário", "Data/Hora"])

    for processo in processos:
        ws.append([
            processo.serial_material.serial,
            processo.etapa,
            processo.status,
            processo.usuario_responsavel.username if processo.usuario_responsavel else "N/A",
            processo.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    # Configurar resposta como arquivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="relatorio_rastreabilidade.xlsx"'
    wb.save(response)
    return response
