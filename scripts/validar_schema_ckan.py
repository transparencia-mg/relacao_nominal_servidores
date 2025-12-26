#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Valida os arquivos do dataset no dados.mg
contra schemas Frictionless.

- Validação direta via URL (CKAN)
- Fail-fast (CI/CD)
- Seguro para CSVs grandes (limit_rows)
"""

import requests
import sys
import re
from pathlib import Path
from frictionless import validate

# ===============================
# CONFIGURAÇÕES
# ===============================

CKAN_HOST = "https://dados.mg.gov.br"
DATASET_NAME = "relacao_nominal_servidores"

HEADERS = {
    "User-Agent": "transparencia-mg/schema-validator",
    "Accept": "application/json"
}

BASE_DIR = Path(__file__).resolve().parent.parent

SCHEMA_DADOS_SERV = BASE_DIR / "schemas" / "dados_serv.schema.json"

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def get_resources():
    url = f"{CKAN_HOST}/api/3/action/package_show"
    r = requests.get(
        url,
        params={"id": DATASET_NAME},
        headers=HEADERS,
        timeout=30
    )
    r.raise_for_status()
    return r.json()["result"]["resources"]


def validar_recurso(nome, url, schema_path):
    print(f"📄 Validando {nome}")

    report = validate(
        url,
        schema=schema_path,
        limit_rows=1000,   # 🔑 essencial para CSVs grandes
        timeout=300
    )

    if not report.valid:
        print("❌ ERRO DE SCHEMA")
        for e in report.flatten(["rowPosition", "fieldName", "message"]):
            print("   ", e)
        return False

    print("✅ OK")
    return True


# ===============================
# MAIN
# ===============================

def main():
    print("🔎 Buscando resources no CKAN")
    resources = get_resources()

    erros = 0

    for r in resources:
        nome = r.get("name", "")
        url = r.get("url")

        if not nome or not url:
            continue

        # Valida apenas dados_serv_YYYYMM.csv
        if re.match(r"^dados_serv_\d{6}\.csv$", nome):
            if not validar_recurso(nome, url, SCHEMA_DADOS_SERV):
                erros += 1
        else:
            print(f"⏭️ Ignorado (fora do escopo): {nome}")

    if erros > 0:
        sys.exit(f"\n❌ {erros} arquivo(s) com erro de schema")

    print("\n🎉 Todos os arquivos válidos")


if __name__ == "__main__":
    main()


