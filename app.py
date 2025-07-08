from flask import Flask, jsonify, send_file, request
from pathlib import Path
import datetime as dt
import os
import sys

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from generators import seed, rd, erp

app = Flask(__name__)

# Configuração base
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        "status": "healthy",
        "message": "Rochalake Data API está funcionando!",
        "timestamp": dt.datetime.now().isoformat()
    })

@app.route('/api/generate-all', methods=['POST'])
def generate_all():
    """Gera todos os dados sintéticos (organizações, deals, ERP)"""
    try:
        today_folder = DATA_DIR / dt.date.today().isoformat()
        today_folder.mkdir(parents=True, exist_ok=True)
        
        # 1. Organizações & Contatos
        orgs, contacts = seed.run(today_folder, n_org=1000)
        
        # 2. CRM – RD Station
        deals = rd.run(today_folder, orgs, dt.date(2025, 1, 1), dt.date(2025, 6, 30))
        
        # 3. ERP – Oracle NetSuite (somente oportunidades ganhas)
        deals_won = [d for d in deals if d["status"] == "won"]
        invoices, payments, gls = erp.generate_erp(deals_won, today_folder)
        
        # Lista os arquivos gerados
        files = []
        if today_folder.exists():
            files = [f.name for f in today_folder.glob("*.csv")]
        
        return jsonify({
            "status": "success",
            "message": "Todos os dados foram gerados com sucesso!",
            "generated_files": files,
            "stats": {
                "organizations": len(orgs),
                "contacts": len(contacts),
                "deals": len(deals),
                "deals_won": len(deals_won),
                "invoices": len(invoices),
                "payments": len(payments),
                "gl_entries": len(gls)
            },
            "data_folder": str(today_folder),
            "timestamp": dt.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar dados: {str(e)}"
        }), 500

@app.route('/api/generate-organizations', methods=['POST'])
def generate_organizations():
    """Gera apenas organizações e contatos"""
    try:
        today_folder = DATA_DIR / dt.date.today().isoformat()
        today_folder.mkdir(parents=True, exist_ok=True)
        
        n_org = 1000
        if request.is_json and request.json:
            n_org = request.json.get('n_organizations', 1000)
        orgs, contacts = seed.run(today_folder, n_org=n_org)
        
        return jsonify({
            "status": "success",
            "message": f"Geradas {len(orgs)} organizações e {len(contacts)} contatos",
            "files": ["organizations_rd.csv", "contacts_rd.csv"],
            "data_folder": str(today_folder),
            "timestamp": dt.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar organizações: {str(e)}"
        }), 500

@app.route('/api/generate-deals', methods=['POST'])
def generate_deals():
    """Gera deals/oportunidades do CRM"""
    try:
        today_folder = DATA_DIR / dt.date.today().isoformat()
        today_folder.mkdir(parents=True, exist_ok=True)
        
        # Primeiro precisa das organizações
        orgs, _ = seed.run(today_folder, n_org=1000)
        
        # Gera os deals
        deals = rd.run(today_folder, orgs, dt.date(2025, 1, 1), dt.date(2025, 6, 30))
        
        return jsonify({
            "status": "success",
            "message": f"Gerados {len(deals)} deals/oportunidades",
            "files": ["deals_rd.csv"],
            "data_folder": str(today_folder),
            "timestamp": dt.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar deals: {str(e)}"
        }), 500

@app.route('/api/generate-erp', methods=['POST'])
def generate_erp_data():
    """Gera dados do ERP (faturas, pagamentos, GL)"""
    try:
        today_folder = DATA_DIR / dt.date.today().isoformat()
        today_folder.mkdir(parents=True, exist_ok=True)
        
        # Primeiro precisa das organizações e deals
        orgs, _ = seed.run(today_folder, n_org=1000)
        deals = rd.run(today_folder, orgs, dt.date(2025, 1, 1), dt.date(2025, 6, 30))
        
        # Filtra apenas deals ganhos
        deals_won = [d for d in deals if d["status"] == "won"]
        
        # Gera dados ERP
        invoices, payments, gls = erp.generate_erp(deals_won, today_folder)
        
        return jsonify({
            "status": "success",
            "message": f"Gerados {len(invoices)} faturas, {len(payments)} pagamentos, {len(gls)} lançamentos GL",
            "files": ["invoices_netsuite.csv", "payments_netsuite.csv", "gl_netsuite.csv"],
            "data_folder": str(today_folder),
            "timestamp": dt.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar dados ERP: {str(e)}"
        }), 500

@app.route('/api/files', methods=['GET'])
def list_files():
    """Lista todos os arquivos CSV disponíveis"""
    try:
        files_info = []
        
        for date_folder in DATA_DIR.glob("*"):
            if date_folder.is_dir():
                for csv_file in date_folder.glob("*.csv"):
                    files_info.append({
                        "filename": csv_file.name,
                        "date": date_folder.name,
                        "path": str(csv_file.relative_to(DATA_DIR)),
                        "size_bytes": csv_file.stat().st_size,
                        "download_url": f"/api/download/{date_folder.name}/{csv_file.name}"
                    })
        
        return jsonify({
            "status": "success",
            "files": files_info,
            "total_files": len(files_info),
            "timestamp": dt.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao listar arquivos: {str(e)}"
        }), 500

@app.route('/api/download/<date>/<filename>', methods=['GET'])
def download_file(date, filename):
    """Baixa um arquivo CSV específico"""
    try:
        file_path = DATA_DIR / date / filename
        
        if not file_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Arquivo não encontrado: {filename}"
            }), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao baixar arquivo: {str(e)}"
        }), 500

@app.route('/api/download/latest/<filename>', methods=['GET'])
def download_latest_file(filename):
    """Baixa a versão mais recente de um arquivo"""
    try:
        # Encontra a pasta mais recente
        date_folders = [f for f in DATA_DIR.glob("*") if f.is_dir()]
        if not date_folders:
            return jsonify({
                "status": "error",
                "message": "Nenhum arquivo encontrado"
            }), 404
        
        latest_folder = max(date_folders, key=lambda x: x.name)
        file_path = latest_folder / filename
        
        if not file_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Arquivo não encontrado: {filename}"
            }), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao baixar arquivo: {str(e)}"
        }), 500

@app.route('/api/info', methods=['GET'])
def api_info():
    """Informações sobre a API e endpoints disponíveis"""
    endpoints = {
        "generate": {
            "POST /api/generate-all": "Gera todos os dados (organizações, deals, ERP)",
            "POST /api/generate-organizations": "Gera apenas organizações e contatos",
            "POST /api/generate-deals": "Gera deals/oportunidades do CRM",
            "POST /api/generate-erp": "Gera dados do ERP (faturas, pagamentos, GL)"
        },
        "download": {
            "GET /api/files": "Lista todos os arquivos CSV disponíveis",
            "GET /api/download/<date>/<filename>": "Baixa arquivo específico por data",
            "GET /api/download/latest/<filename>": "Baixa versão mais recente do arquivo"
        },
        "utility": {
            "GET /api/health": "Verificação de saúde da API",
            "GET /api/info": "Informações sobre a API"
        }
    }
    
    return jsonify({
        "api_name": "Rochalake Data API",
        "version": "1.0.0",
        "description": "API para gerar e baixar dados sintéticos do projeto Rochalake",
        "endpoints": endpoints,
        "data_types": [
            "organizations_rd.csv - Organizações base",
            "contacts_rd.csv - Contatos das organizações", 
            "deals_rd.csv - Oportunidades/deals do CRM",
            "invoices_netsuite.csv - Faturas do ERP",
            "payments_netsuite.csv - Pagamentos do ERP",
            "gl_netsuite.csv - Lançamentos contábeis"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)