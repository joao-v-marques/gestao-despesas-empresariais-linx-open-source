import os
from fpdf import FPDF

def gerar_pdf(solicitacao, usuario_aprovador, usuario_solicitante):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Comprovante de Aprovação", ln=True, align='C')
    pdf.cell(200, 10, txt=f"ID da Solicitação: {solicitacao['id']}", ln=True)
    pdf.cell(200, 10, txt=f"Empresa/Revenda: {solicitacao['empresa']}.{solicitacao['revenda']}", ln=True)
    pdf.cell(200, 10, txt=f"Usuário Solicitante: {usuario_solicitante}", ln=True)
    pdf.cell(200, 10, txt=f"Departamento: {solicitacao['departamento']}", ln=True)
    pdf.cell(200, 10, txt=f"Descrição: {solicitacao['descricao']}", ln=True)
    pdf.cell(200, 10, txt=f"Valor: R$ {solicitacao['valor']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Aprovado por: {usuario_aprovador}", ln=True)

    base_dir = "C:/processo_despesas_kato/static/pdf"
    os.makedirs(base_dir, exist_ok=True)
    pdf_path = os.path.join(base_dir, f'solicitacao_{solicitacao['id']}.pdf')
    pdf.output(pdf_path)
    return pdf_path