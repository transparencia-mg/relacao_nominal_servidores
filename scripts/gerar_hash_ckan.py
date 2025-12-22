#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

HASHES_FILE = BASE_DIR / "datapackage" / "hashes.json"
RESOURCES_FILE = BASE_DIR / "datapackage" / "resources.json"
OUTPUT_FILE = BASE_DIR / "datapackage" / "datapackage.json"

SCHEMA_DADOS_SERV = {
    "fields": [
        {"name": "ano_mes", "type": "string"},
        {"name": "masp", "type": "string"},
        {"name": "adm", "type": "string"},
        {"name": "nome", "type": "string"},
        {"name": "siglaefetivo", "type": "string"},
        {"name": "nmefetivo", "type": "string"},
        {"name": "cdcomi", "type": "string"},
        {"name": "desccomi", "type": "string"},
        {"name": "cd_funcao_gratif_gte", "type": "string"},
        {"name": "desc_funcao_gratif_gte", "type": "string"},
        {"name": "carga_horaria", "type": "string"},
        {"name": "descsitserv", "type": "string"}
    ],
    "missingValues": [""]
}

def main():
    if not HASHES_FILE.exists():
        raise RuntimeError("hashes.json não encontrado")

    if not RESOURCES_FILE.exists():
        raise RuntimeError("resources.json não encontrado")

    hashes = json.loads(HASHES_FILE.read_text(encoding="utf-8"))
    resources_ckan = json.loads(RESOURCES_FILE.read_text(encoding="utf-8"))

    resources = []

    for r in resources_ckan:
        name = r.get("name")
        url = r.get("url")

        if not name or not url:
            continue

        if not name.startswith("dados_serv_") or not name.endswith(".csv"):
            continue

        hash_value = hashes.get(name)
        if not hash_value:
            continue

        resource = {
            "name": name.replace(".csv", ""),
            "title": f"Relação Nominal de Servidores – {name[-10:-4]}",
            "format": "csv",
            "mediatype": "text/csv",
            "path": url,
            "hash": hash_value,
            "schema": SCHEMA_DADOS_SERV
        }

        resources.append(resource)

    datapackage = {
        "name": "relacao-nominal-servidores",
        "title": "Relação Nominal de Servidores do Estado de Minas Gerais",
        "profile": "data-package",
        "resources": resources
    }

    OUTPUT_FILE.write_text(
        json.dumps(datapackage, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"✅ datapackage.json gerado com {len(resources)} recursos")

if __name__ == "__main__":
    main()
