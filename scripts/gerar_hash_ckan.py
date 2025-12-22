#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gera hash SHA256 de TODOS os CSVs do dataset no dados.mg,
com tolerância a falhas (502, timeout, etc).
"""

import json
import hashlib
import requests
import time
from pathlib import Path

CKAN_HOST = "https://dados.mg.gov.br"
DATASET_NAME = "relacao_nominal_servidores"
DATAPACKAGE = Path("datapackage/datapackage.json")

HEADERS = {
    "User-Agent": "transparencia-mg/hash-generator",
    "Accept": "application/json"
}

MAX_RETRIES = 3
RETRY_DELAY = 5  # segundos

from typing import Optional

def sha256_from_url(url: str) -> Optional[str]:
    for tentativa in range(1, MAX_RETRIES + 1):
        try:
            h = hashlib.sha256()
            with requests.get(url, stream=True, headers=HEADERS, timeout=600) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        h.update(chunk)
            return f"sha256:{h.hexdigest()}"
        except Exception as e:
            print(f"   ⚠️ Tentativa {tentativa}/{MAX_RETRIES} falhou: {e}")
            if tentativa < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    return None

def get_resources_from_ckan():
    url = f"{CKAN_HOST}/api/3/action/package_show"
    r = requests.get(url, params={"id": DATASET_NAME}, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.json()["result"]["resources"]

def is_csv(resource):
    name = (resource.get("name") or "").lower()
    fmt = (resource.get("format") or "").lower()
    url = (resource.get("url") or "").lower()

    return (
        fmt == "csv"
        or name.endswith(".csv")
        or url.endswith(".csv")
    )

def main():
    print("🔎 Consultando CKAN...")
    resources = get_resources_from_ckan()

    print(f"📦 {len(resources)} resources encontrados")

    dp = {
        "name": "relacao-nominal-servidores-mg",
        "title": "Relação Nominal de Servidores – Minas Gerais",
        "resources": []
    }

    falhas = []

    for r in resources:
        nome = r.get("name") or r["id"]

        if not is_csv(r):
            print(f"⏭️ Ignorado (não CSV): {nome}")
            continue

        url = r.get("url")
        if not url:
            print(f"⏭️ Ignorado (sem URL): {nome}")
            continue

        print(f"📄 Processando: {nome}")
        hash_value = sha256_from_url(url)

        if not hash_value:
            print(f"❌ Falha definitiva: {nome}")
            falhas.append(nome)
            continue

        dp["resources"].append({
            "name": nome,
            "title": r.get("description") or nome,
            "format": "CSV",
            "url": url,
            "hash": hash_value
        })

        print(f"   ↳ {hash_value}")

    DATAPACKAGE.parent.mkdir(exist_ok=True)
    DATAPACKAGE.write_text(
        json.dumps(dp, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\n✅ Hash gerado para todos os CSVs possíveis")

    if falhas:
        print("\n⚠️ Arquivos que não puderam ser processados:")
        for f in falhas:
            print(f" - {f}")

        print("\n👉 Recomendação: rodar novamente mais tarde")
    else:
        print("\n🎉 Nenhuma falha encontrada")

if __name__ == "__main__":
    main()
