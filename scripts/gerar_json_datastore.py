#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from pathlib import Path
from collections import defaultdict

# ===============================
# CONFIGURAÇÕES
# ===============================

RESOURCE_ID = "74e9fe88-a476-4061-95d0-5091ec131b3f"
CKAN_URL = "https://dados.mg.gov.br/api/3/action/datastore_search"

LIMITE = 500

OUTPUT_DIR = Path("docs/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ARQ_VISAO_GERAL = OUTPUT_DIR / "visao_geral.json"
ARQ_DETALHADO = OUTPUT_DIR / "detalhado.json"

# ===============================
# FUNÇÃO PARA BUSCAR TODOS OS DADOS
# ===============================

def buscar_todos_os_registros():
    registros = []
    offset = 0

    print("🔎 Buscando dados do DataStore CKAN...")

    while True:
        params = {
            "resource_id": RESOURCE_ID,
            "limit": LIMITE,
            "offset": offset
        }

        resp = requests.get(CKAN_URL, params=params, timeout=60)
        resp.raise_for_status()

        data = resp.json()

        if not data.get("success"):
            raise RuntimeError("Resposta inválida do CKAN")

        batch = data["result"]["records"]
        registros.extend(batch)

        print(f"   ➕ {len(batch)} registros (offset {offset})")

        if len(batch) < LIMITE:
            break

        offset += LIMITE

    print(f"✅ Total de registros: {len(registros)}")
    return registros


# ===============================
# GERAR VISÃO GERAL
# ===============================

def gerar_visao_geral(registros):
    agrupado = defaultdict(lambda: {"sigla": "", "nome": "", "total": 0})

    for r in registros:
        sigla = r.get("sigla_instituicao_lotacao") or "N/I"
        nome = r.get("desc_instituicao_lotacao") or "Não informado"

        agrupado[sigla]["sigla"] = sigla
        agrupado[sigla]["nome"] = nome
        agrupado[sigla]["total"] += 1

    return list(agrupado.values())


# ===============================
# GERAR DADOS DETALHADOS
# ===============================

def gerar_detalhado(registros):
    detalhado = []

    for r in registros:
        detalhado.append({
            "masp": r.get("masp"),
            "nome": r.get("nome"),
            "orgao": r.get("sigla_instituicao_lotacao"),
            "cargo": r.get("nmefetivo"),
            "carga_horaria": r.get("carga_horaria"),
            "situacao": r.get("descsitserv")
        })

    return detalhado


# ===============================
# MAIN
# ===============================

def main():
    registros = buscar_todos_os_registros()

    visao_geral = gerar_visao_geral(registros)
    detalhado = gerar_detalhado(registros)

    ARQ_VISAO_GERAL.write_text(
        json.dumps(visao_geral, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    ARQ_DETALHAD_
