#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Valida TODOS os arquivos do dataset no dados.mg
contra schemas Frictionless.
Se algum falhar → erro (workflow para).
"""

import requests
import sys
from frictionless import validate

CKAN_HOST = "https://dados.mg.gov.br"
DATASET_NAME = "relacao_nominal_servidores"

HEADERS = {
    "User-Agent": "transparencia-mg/schema-validator",
    "Accept": "application/json"
}

SCHEMA_MAP = {
    "dados_serv": "schemas/dados_serv.schema.json",
    "dm_tempo_diario": "schemas/dm_tempo_diario.schema.json"
}

def get_resources():
    url = f"{CKAN_HOST}/api/3/action/package_show"
    r = requests.get(url, params={"id": DATASET_NAME}, headers=HEADERS)
    r.raise_for_status()
    return r.json()["result"]["resources"]

def main():
    print("🔎 Buscando resources no CKAN")
    resources = get_resources()

    erros = 0

    for r in resources:
        nome = r.get("name", "")
        url = r.get("url")

        if not url:
            continue

        schema = None
        for prefixo, schema_path in SCHEMA_MAP.items():
            if nome.startswith(prefixo):
                schema = schema_path

        if not schema:
            print(f"⏭️ Ignorado (sem schema): {nome}")
            continue

        print(f"📄 Validando {nome}")
        report = validate(url, schema=schema)

        if not report.valid:
            erros += 1
            print("❌ ERRO DE SCHEMA")
            for e in report.flatten(["rowPosition", "fieldName", "message"]):
                print("   ", e)
        else:
            print("✅ OK")

    if erros > 0:
        sys.exit(f"❌ {erros} arquivo(s) com erro de schema")

    print("🎉 Todos os arquivos válidos")

if __name__ == "__main__":
    main()
