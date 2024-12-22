import openpyxl
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cme_app.models import Processo


@api_view(['GET'])
def gerar_relatorio_pdf(request):
    serial = request.query_params.get('serial', None)

    # Obter dados filtrados
    if serial:
        processos = Processo.objects.filter(serial_material__serial=serial)
        if not processos.exists():
            return Response({"detail": "Nenhum processo encontrado para o serial especificado."}, status=404)
    else:
        processos = Processo.objects.all()
        if not processos.exists():
            return Response({"detail": "Nenhum processo encontrado no sistema."}, status=404)

    # Configurar resposta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_rastreabilidade.pdf"'

    # Criar PDF
    p = canvas.Canvas(response)
    p.drawString(100, 800, "Relatório de Rastreabilidade")
    y = 750
    for processo in processos:
        p.drawString(
            50,
            y,
            f"Serial: {processo.serial_material.serial} | "
            f"Etapa: {processo.etapa} | "
            f"Status: {processo.status} | "
            f"Usuário: {processo.usuario_responsavel.username if processo.usuario_responsavel else 'N/A'} | "
            f"Data: {processo.data_hora.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        y -= 20
        if y < 50:  # Adiciona nova página se necessário
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    return response


@api_view(['GET'])
def gerar_relatorio_xlsx(request):
    serial = request.query_params.get('serial', None)

    # Obter dados filtrados
    if serial:
        processos = Processo.objects.filter(serial_material__serial=serial)
        if not processos.exists():
            return Response({"detail": "Nenhum processo encontrado para o serial especificado."}, status=404)
    else:
        processos = Processo.objects.all()
        if not processos.exists():
            return Response({"detail": "Nenhum processo encontrado no sistema."}, status=404)

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
    response['Content-Disposition'] = 'attachment; filename="relatorio_rastreabilidade.xlsx"'
    wb.save(response)
    return response
