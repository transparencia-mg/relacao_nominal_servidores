#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exporta views do PostgreSQL para CSV.

Usado para:
- gerar arquivos consumidos pelo GitHub Pages
- manter dados derivados fora do banco
- não versionar dados brutos grandes

Views esperadas:
- servidores_visao_geral
- servidores_detalhado
"""

import os
import psycopg2
from pathlib import Path

# ===============================
# CONFIGURAÇÕES
# ===============================

VIEWS = {
    "servidores_visao_geral": "servidores_visao_geral.csv",
    "servidores_detalhado": "servidores_detalhado.csv"
}

OUTPUT_DIR = Path("data")

# ===============================
# CONEXÃO
# ===============================

def get_conn():
    return psycopg2.connect(
        host=os.environ["PG_HOST"],
        port=os.environ.get("PG_PORT", "5432"),
        dbname=os.environ["PG_DB"],
        user=os.environ["PG_USER"],
        password=os.environ["PG_PASSWORD"]
    )

# ===============================
# EXPORTAÇÃO
# ===============================

def exportar_view(conn, view_name, output_file):
    print(f"📄 Exportando {output_file}")

    with conn.cursor() as cur:
        with open(output_file, "w", encoding="utf-8", newline="") as f:
            cur.copy_expert(
                f"""
                COPY (
                    SELECT * FROM {view_name}
                )
                TO STDOUT
                WITH CSV
                HEADER
                DELIMITER ';'
                ENCODING 'UTF8'
                """,
                f
            )

    print(f"✅ {output_file} gerado")

# ===============================
# MAIN
# ===============================

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    conn = get_conn()

    try:
        for view, filename in VIEWS.items():
            output_path = OUTPUT_DIR / filename
            exportar_view(conn, view, output_path)

        print("🎉 Exportação das views concluída com sucesso")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
