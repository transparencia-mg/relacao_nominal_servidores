#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Publica/atualiza APENAS METADADOS do dataset no CKAN
usando o datapackage.json gerado automaticamente.

- Não publica CSV
- Não altera dados
- Fail-fast para CI/CD
"""

import subprocess
import sys
import os
import shutil

DATAPACKAGE_PATH = "datapackage/datapackage.json"

def main():
    ckan_host = os.environ.get("CKAN_HOST")
    ckan_key = os.environ.get("CKAN_KEY")

    if not ckan_host or not ckan_key:
        sys.exit("❌ CKAN_HOST ou CKAN_KEY não configurados")

    if not os.path.exists(DATAPACKAGE_PATH):
        sys.exit(f"❌ {DATAPACKAGE_PATH} não encontrado")

    # Garante que dpckan está disponível
    if not shutil.which("dpckan"):
        sys.exit("❌ dpckan não encontrado no PATH")

    cmd = [
        "dpckan",
        "dataset",
        "update",
        "--ckan-host", ckan_host,
        "--ckan-key", ckan_key,
        "--datapackage", DATAPACKAGE_PATH
    ]

    print("🚀 Atualizando metadados no CKAN")
    print("🔗 Dataset:", ckan_host)
    print("📦 Datapackage:", DATAPACKAGE_PATH)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"❌ Erro ao atualizar metadados no CKAN (dpckan exit {e.returncode})")

    print("✅ Metadados atualizados com sucesso")

if __name__ == "__main__":
    main()


