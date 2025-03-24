from fastapi import FastAPI, Response
from models import SimulationInput, SimulationOutput
from utils import generate_cash_flow_chart, generate_pdf_report
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = FastAPI()

# Configura pastas de HTML e CSS
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def render_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/simulate/", response_model=SimulationOutput)
def simulate(data: SimulationInput):
    months_projection = []
    balance = data.current_savings
    month_names = []

    today = datetime.date.today()
    for i in range(6):
        next_month = today + datetime.timedelta(days=30 * i)
        month_str = next_month.strftime("%B")
        income = data.monthly_income
        expenses = sum(data.monthly_expanses.values())
        net = income - expenses + data.monthly_investiment
        balance += net
        months_projection.append({
            "month": month_str,
            "projected_balance": round(balance, 2)
        })
        month_names.append(month_str)

    suggestions = []
    if expenses > income:
        suggestions.append("Atenção: Suas despesas superam sua renda!")
    else:
        suggestions.append("Parabéns! Você está economizando mensalmente.")

    if data.monthly_investiment < 0.1 * data.monthly_income:
        suggestions.append("Considere investir pelo menos 10% da sua renda.")

    return {
        "cash_flow_projection": months_projection,
        "suggestions": suggestions
    }


@app.get("/report/{user_id}")
def get_report(user_id: str):
    projection = [
        {"month": "Abril", "projected_balance": 12000},
        {"month": "Maio", "projected_balance": 13500}
    ]
    suggestions = ["Economize mais de R$200/mês.", "Investimento em renda fixa recomendado."]
    chart_base64 = generate_cash_flow_chart(projection)

    return {
        "cash_flow_projection": projection,
        "chart": chart_base64,
        "suggestions": suggestions
    }


@app.get("/export/{user_id}")
def export_pdf(user_id: str):
    # Aqui você vai gerar a projeção para o PDF
    projection = [
        {"month": "Abril", "projected_balance": 12000},
        {"month": "Maio", "projected_balance": 13500}
    ]
    suggestions = ["Economize mais de R$200/mês.", "Investimento em renda fixa recomendado."]
    
    # Função que gera o PDF a partir da projeção e sugestões
    pdf_buffer = generate_pdf_report(projection, suggestions)

    headers = {'Content-Disposition': f'attachment; filename="report_{user_id}.pdf"'}
    return Response(content=pdf_buffer.read(), media_type="application/pdf", headers=headers)


# Função para gerar o PDF com a projeção e sugestões
# def generate_pdf_report(projection, suggestions):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(100, 750, "Relatório de Projeção Financeira")
    
    # Exibir a projeção dos meses e saldos
    y_position = 730
    c.drawString(100, y_position, "Projeção de Fluxo de Caixa:")
    y_position -= 20
    for proj in projection:
        c.drawString(100, y_position, f"{proj['month']}: R$ {proj['projected_balance']}")
        y_position -= 20

    # Adicionar sugestões
    y_position -= 40
    c.drawString(100, y_position, "Sugestões:")
    y_position -= 20
    for suggestion in suggestions:
        c.drawString(100, y_position, f"- {suggestion}")
        y_position -= 20

    # Finalizar e salvar o PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
@app.get("/export/{user_id}")
def export_pdf(user_id: str):
    projection = [
        {"month": "Abril", "projected_balance": 12000},
        {"month": "Maio", "projected_balance": 13500}
    ]
    suggestions = ["Economize mais de R$200/mês.", "Investimento em renda fixa recomendado."]
    pdf_buffer = generate_pdf_report(projection, suggestions)

    headers = {'Content-Disposition': f'attachment; filename="report_{user_id}.pdf"'}
    return Response(content=pdf_buffer.read(), media_type="application/pdf", headers=headers)
