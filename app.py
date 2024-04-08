from flask import Flask, render_template, request, redirect
import openai
from dotenv import load_dotenv
import os
import re
from werkzeug.utils import secure_filename 
from docx import Document

app = Flask(__name__)

#Credencial para uso da API do ChatGPT
OPENAI_API_KEY= os.environ["OPENAI_API_KEY"]

from flask import Flask, render_template, request, redirect
from docx import Document


# Função para ler a transcrição do documento DOCX
def ler_transcricao():
    document = Document("transcricao.docx")
    texto = ""
    for paragraph in document.paragraphs:
        texto += paragraph.text + "\n"
    return texto

# Função para gerar o título da matéria
def gerar_titulo(transcricao, nome_especialista):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": f"Você é um jornalista escrevendo uma matéria sobre uma reunião da equipe Santo Caos que aconteceu hoje. Com base nesta transcrição de reunião: {transcricao}, gerar um título curto e atraente para a matéria. Cite o nome do especialista {especialista} que comentou sobre a reunião." }
        ]
    )
    return resposta.choices[0].message["content"]

# Função para gerar o lide da matéria
def gerar_lide(transcricao, titulo):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": f"Você é um jornalista escrevendo uma matéria sobre uma reunião da equipe Santo Caos que aconteceu hoje. Com base na transcrição de reunião {transcricao}, e no título {titulo}, gere um lide que suporte o título." }
        ]
    )
    return resposta.choices[0].message["content"]

# Função para gerar as informações secundárias da matéria
def gerar_informacoes_secundarias(transcricao, titulo, nome_especialista, consideracoes):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": f"Você é um jornalista escrevendo uma matéria sobre uma reunião da equipe Santo Caos que aconteceu hoje. Com base nesta transcrição de reunião: {transcricao}, e no título gerado {titulo}, escreva a matérias em 3 parágrafos. Mencione em  lugar de destaque do texto o especialista {nome_especialista}, e use as suas seguintes consideraçõe {consideracoes} sobre o que achou da reunião de hoje tanto nas citações, quanto para mudar o tom do texto da matéria. " }
        ]
    )
    return resposta.choices[0].message["content"]


# Rota para a página inicial
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Rota para gerar a matéria
@app.route('/gerar_materia', methods=['POST'])
def gerar_materia():
    transcricao = ler_transcricao()

    # Captura os inputs do usuário
    nome_especialista = request.form['nome_especialista']
    consideracoes = request.form['consideracoes']

    # Chama a função para gerar o título da matéria
    titulo = gerar_titulo(transcricao)

    # Chama as demais funções para gerar as partes da matéria
    lide = gerar_lide(transcricao, titulo)
    informacoes_secundarias = gerar_informacoes_secundarias(transcricao, titulo, nome_especialista, consideracoes)


    # Retorna a página com a matéria gerada
    return render_template('materia.html', titulo=titulo, lide=lide, informacoes_secundarias=informacoes_secundarias)

if __name__ == '__main__':
    app.run(debug=True)
