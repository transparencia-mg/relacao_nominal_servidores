from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from db import get_conn

app = FastAPI(
    title="API Homologação – Relação Nominal de Servidores",
    version="1.0.0"
)

# 🔓 CORS liberado apenas para homologação
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # depois restrinja
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# GET /periodos
# ============================================
@app.get("/periodos")
def listar_periodos():
    """
    Retorna os períodos disponíveis no banco
    """
    sql = """
        SELECT DISTINCT periodo_referencia
        FROM vw_servidores_detalhado
        ORDER BY periodo_referencia;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return [r["periodo_referencia"] for r in rows]


# ============================================
# GET /servidores/visao-geral
# ============================================
@app.get("/servidores/visao-geral")
def visao_geral(periodo: str = Query(..., example="2025-11")):
    sql = """
        SELECT
            sigla_instituicao_lotacao AS sigla,
            desc_instituicao_lotacao  AS nome,
            COUNT(*)                 AS total
        FROM vw_servidores_detalhado
        WHERE periodo_referencia = %s
        GROUP BY 1, 2
        ORDER BY total DESC;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (periodo,))
            rows = cur.fetchall()

    return {
        "periodo": periodo,
        "dados": rows
    }


# ============================================
# GET /servidores/detalhado
# ============================================
@app.get("/servidores/detalhado")
def detalhado(
    periodo: str = Query(..., example="2025-11"),
    limit: int = 1000,
    offset: int = 0
):
    sql = """
        SELECT
            masp,
            nome,
            sigla_instituicao_lotacao AS orgao,
            nmefetivo                AS cargo,
            carga_horaria,
            descsitserv              AS situacao
        FROM vw_servidores_detalhado
        WHERE periodo_referencia = %s
        ORDER BY nome
        LIMIT %s OFFSET %s;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (periodo, limit, offset))
            rows = cur.fetchall()

    return {
        "periodo": periodo,
        "limit": limit,
        "offset": offset,
        "dados": rows
    }
