import os
from fpdf import FPDF

def gerar_pdf(solicitacao, usuario_aprovador):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Comprovante de Aprovação", ln=True, align='C')
    pdf.cell(200, 10, txt=f"ID da Solicitação: {solicitacao.id}", ln=True)
    pdf.cell(200, 10, txt=f"Empresa/Revenda: {solicitacao.EMPRESA}.{solicitacao.REVENDA}", ln=True)
    pdf.cell(200, 10, txt=f"Usuário Solicitante: {solicitacao.USUARIO_SOLICITANTE}", ln=True)
    pdf.cell(200, 10, txt=f"Departamento: {solicitacao.DEPARTAMENTO}", ln=True)
    pdf.cell(200, 10, txt=f"Tipo de Despesa: {solicitacao.TIPO_DESPESA}", ln=True)
    pdf.cell(200, 10, txt=f"Descrição: {solicitacao.DESCRICAO}", ln=True)
    pdf.cell(200, 10, txt=f"Valor: R$ {solicitacao.VALOR:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Aprovado por: {usuario_aprovador}", ln=True)

    pdf_dir = os.path.join('static', 'pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"solicitacao_{solicitacao.id}.pdf")
    pdf.output(pdf_path)
    return pdf_path