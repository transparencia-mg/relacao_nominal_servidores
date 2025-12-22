#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Publica/atualiza APENAS METADADOS do dataset no CKAN
(usando datapackage.json gerado automaticamente).
"""

import subprocess
import sys
import os

def main():
    ckan_host = os.environ.get("CKAN_HOST")
    ckan_key = os.environ.get("CKAN_KEY")

    if not ckan_host or not ckan_key:
        sys.exit("❌ CKAN_HOST ou CKAN_KEY não configurados")

    cmd = [
        "dpckan",
        "dataset",
        "update",
        "--ckan-host", ckan_host,
        "--ckan-key", ckan_key,
        "--datapackage", "datapackage/datapackage.json"
    ]

    print("🚀 Atualizando metadados no CKAN")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        sys.exit("❌ Erro ao atualizar metadados no CKAN")

    print("✅ Metadados atualizados com sucesso")

if __name__ == "__main__":
    main()

