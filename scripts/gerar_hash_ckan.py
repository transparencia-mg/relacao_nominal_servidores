#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import hashlib
import json
from pathlib import Path
import time

# ===============================
# CONFIGURAÇÕES
# ===============================

CKAN_HOST = "https://dados.mg.gov.br"
DATASET_ID = "relacao_nominal_servidores"

BASE_DIR = Path(__file__).resolve().parent.parent
DATAPACKAGE_DIR = BASE_DIR / "datapackage"

RESOURCES_FILE = DATAPACKAGE_DIR / "resources.json"
HASHES_FILE = DATAPACKAGE_DIR / "hashes.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (datapackage-generator)",
    "Accept": "application/json"
}

# ===============================
# FUNÇÕES
# ===============================

def fetch_resources_from_ckan():
    url = f"{CKAN_HOST}/api/3/action/package_show"
    resp = requests.get(
        url,
        params={"id": DATASET_ID},
        headers=HEADERS,
        timeout=30
    )

    print("🌐 URL:", resp.url)
    print("📡 Status HTTP:", resp.status_code)

    if resp.status_code != 200:
        raise RuntimeError(f"Erro HTTP {resp.status_code} ao acessar CKAN")

    data = resp.json()
    return data["result"]["resources"]

def sha256_from_url(url):
    h = hashlib.sha256()
    with requests.get(url, stream=True, headers=HEADERS, timeout=180) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                h.update(chunk)
    return "sha256:" + h.hexdigest()

# ===============================
# MAIN
# ===============================

def main():
    print("📁 Diretório base:", BASE_DIR)
    DATAPACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    print("🔎 Buscando resources no CKAN...")
    resources = fetch_resources_from_ckan()

    # Salva cache de metadados
    RESOURCES_FILE.write_text(
        json.dumps(resources, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"✅ resources.json salvo ({len(resources)} recursos)")

    hashes = {}

    for r in resources:
        name = r.get("name")
        url = r.get("url")

        if not name or not url:
            continue

        # só calcula hash de CSVs
        if not name.endswith(".csv"):
            continue

        print(f"📄 Calculando hash: {name}")
        try:
            hashes[name] = sha256_from_url(url)
            print("   ↳ OK")
            time.sleep(1)  # evita rate limit
        except Exception as e:
            print(f"   ⚠️ ERRO: {e}")

    HASHES_FILE.write_text(
        json.dumps(hashes, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"✅ hashes.json salvo ({len(hashes)} arquivos)")

if __name__ == "__main__":
    main()
