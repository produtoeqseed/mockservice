
from flask import Flask, request, jsonify
from flask_cors import CORS
from faker import Faker
import random
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
CORS(app)
fake = Faker('pt_BR')

def gerar_investidor_completo(qtd_clientes=1):
    dados = []

    for _ in range(qtd_clientes):
        investidor_id = fake.random_int(min=100000, max=999999)
        nome = fake.name()
        qtd_rodadas = random.randint(1, 3)
        valor_total = round(random.uniform(5000, 200000), 2)
        iss_geral = round(random.uniform(0, 10), 2)

        empresas = []
        for _ in range(qtd_rodadas):
            empresa_id = fake.random_int(min=80000, max=89999)
            nome_empresa = fake.company()
            cnpj = fake.cnpj()
            categoria = random.choice(['Fintech', 'Agtech', 'SaaS', 'EduTech'])
            iss_empresa = random.randint(1, 100)
            estagio = random.choice(['Ideação', 'Early-stage', 'Estágio de crescimento'])
            status = random.choice(['Aberta para investir', 'Terminada', 'Exit', 'Writeoff'])
            linkedin = fake.url()
            instagram = fake.url()
            site = fake.url()
            logo = fake.image_url()

            valor_investido = round(random.uniform(5000, 150000), 2)
            percentual_rodada = round(random.uniform(0.1, 5), 4)
            status_inv = random.choice(['Emitido', 'Assinado', 'Cancelado'])
            status_liq = random.choice(['Concluída', 'Em andamento', 'Pendente'])
            data_emissao = fake.date_time_this_year()
            data_assinatura = data_emissao + timedelta(minutes=5)
            link_docusign = fake.url()

            valor_captado = random.randint(500000, 2000000)
            data_ini_liq = data_assinatura + timedelta(days=10)
            data_fim_liq = data_ini_liq + timedelta(days=30)

            documentos = [{
                "nome_arquivo": "Relatório de Oferta",
                "tipo": "Relatórios",
                "trimestre": "1T",
                "ano": 2025,
                "link": fake.url()
            }]

            indicadores = [{
                "nome": "Receita",
                "pilar": "Financeiro",
                "valor": round(random.uniform(100000, 1000000), 2),
                "trimestre": "1T",
                "ano": 2025
            }]

            cartas_ceo = [{
                "trimestre": "1T",
                "ano": 2025,
                "texto": fake.paragraph(nb_sentences=5)
            }]

            empresa = {
                "id": empresa_id,
                "nome_empresa": nome_empresa,
                "cnpj": cnpj,
                "categoria": categoria,
                "iss": iss_empresa,
                "estagio": estagio,
                "status_rodada": status,
                "linkedin": linkedin,
                "instagram": instagram,
                "site": site,
                "logo": logo,
                "investimento": {
                    "valor": valor_investido,
                    "percentual_rodada": percentual_rodada,
                    "status_investimento": status_inv,
                    "status_liquidacao": status_liq,
                    "data_emissao": data_emissao.isoformat(),
                    "data_assinatura": data_assinatura.isoformat(),
                    "link_docusign": link_docusign,
                },
                "rodada": {
                    "valor_captado": valor_captado,
                    "inicio_liquidacao": data_ini_liq.isoformat(),
                    "fim_liquidacao": data_fim_liq.isoformat()
                },
                "documentos": documentos,
                "indicadores": indicadores,
                "cartas_ceo": cartas_ceo
            }

            empresas.append(empresa)

        dados.append({
            "id": investidor_id,
            "nome": nome,
            "numero_de_rodadas": qtd_rodadas,
            "valor_total_investido": valor_total,
            "iss_geral": iss_geral,
            "empresas_investidas": empresas
        })

    return dados

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"mensagem": "API Mock ativa! Use a rota /mock"})

@app.route('/mock', methods=['GET'])
def mock():
    qtd_clientes = int(request.args.get('clientes', 1))
    persistir = request.args.get('persistir', 'false').lower() == 'true'

    if not persistir and os.path.exists("dados_mock.json"):
        with open("dados_mock.json", "r", encoding="utf-8") as f:
            return jsonify(json.load(f))

    dados = gerar_investidor_completo(qtd_clientes)

    if persistir:
        with open("dados_mock.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    return jsonify(dados)

@app.route('/mock/<int:investidor_id>', methods=['GET'])
def buscar_por_id(investidor_id):
    if not os.path.exists("dados_mock.json"):
        return jsonify({"erro": "Nenhum dado persistido ainda"}), 404

    with open("dados_mock.json", "r", encoding="utf-8") as f:
        todos = json.load(f)

    investidor = next((i for i in todos if i["id"] == investidor_id), None)

    if investidor:
        return jsonify(investidor)
    else:
        return jsonify({"erro": f"Investidor {investidor_id} não encontrado"}), 404

if __name__ == '__main__':
    app.run()
