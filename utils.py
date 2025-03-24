import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO
from reportlab.pdfgen import canvas

def generate_cash_flow_chart(projection):
    months = [item['month'] for item in projection]
    balances = [item['projected_balance'] for item in projection]

        
    plt.figure(figsize=(8, 4))
    plt.plot(months, balances, marker=0)
    plt.title('Projeto de Saldo mensal')
    plt.xlabel('Mês')
    plt.ylabel('Saldo (R$)')
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64decode(buf.read()).decode('utf-8')

def generate_pdf_report(projection, suggestions, filename="report.pdf"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica", 14)
    c.drawString(100, 800, "Relatório Financeiro Personalizado")

    y = 750
    for item in projection:
        c.drawString(100, y, f"{item['month']}: R$ {item['projected_balance']:.2f}")
        y -= 20

    y -= 20
    c.drawString(100, y, "Sugestôes:")
    y -= 20  
    for s in suggestions:
        c.drawString(120, y, f"- {s}")
        y -= 20


    c.save()
    buffer.seek(0)
    return buffer







