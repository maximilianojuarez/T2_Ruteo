"""
=============================================================================
ARCHIVO: main.py
PROYECTO: Resiliencia de la Infraestructura de Internet Chilena (Proyecto Yafún)
          frente al Terremoto M 8.8 del Maule (27-02-2010)
FLUJO UNIFICADO EN UN SOLO COMANDO (`python main.py`):
  1. Verifica o construye la topología (`pgr_createTopology`), nodos clave,
     probabilidades de falla sísmica y archivo `main.sql`.
  2. Levanta automáticamente el contenedor Docker PostgreSQL/PostGIS/pgRouting
     (`ruteo_chile_db`) y carga `main.sql`.
  3. Imprime el resumen completo de infraestructura, topología, probabilidades
     de falla y comparación de ATTR (antes y después del sismo M 8.8).
  4. Levanta el servidor web interactivo con Leaflet en http://127.0.0.1:8000.
=============================================================================
"""

import os
import sys
import json
import random
import argparse
import subprocess
from collections import defaultdict
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RED_GEOJSON_PATH = os.path.join(BASE_DIR, "01_infraestructura", "red_troncal_chile.geojson")
NODOS_GEOJSON_PATH = os.path.join(BASE_DIR, "02_nodos_clave", "nodos_clave.geojson")
CATALOGO_NODOS_PATH = os.path.join(BASE_DIR, "02_nodos_clave", "catalogo_nodos_estrategicos.json")
VERTICES_JSON_PATH = os.path.join(BASE_DIR, "03_topologia", "vertices_pgr.json")
ATTR_OP_PATH = os.path.join(BASE_DIR, "04_attr_operacion", "resultados_attr_operacion.json")
SISMO_GEOJSON_PATH = os.path.join(BASE_DIR, "05_terremoto_geojson", "terremoto_8_8_maule.geojson")
ATTR_POST_PATH = os.path.join(BASE_DIR, "09_attr_post_terremoto", "resultados_attr_post_sismo.json")
HTML_INDEX_PATH = os.path.join(BASE_DIR, "10_aplicacion_web", "index.html")
MAIN_SQL_PATH = os.path.join(BASE_DIR, "main.sql")

# Si se ejecuta desde un clon limpio y falta algún archivo generado, construir todo automáticamente
if not (os.path.exists(RED_GEOJSON_PATH) and os.path.exists(MAIN_SQL_PATH) and os.path.exists(CATALOGO_NODOS_PATH)):
    print("[Inicialización] Generando topología, probabilidades, main.sql y métricas ATTR desde Respuesta_T5610...")
    import build_project_data
    build_project_data.main()

with open(RED_GEOJSON_PATH, "r", encoding="utf-8") as f:
    RED_GEOJSON = json.load(f)

with open(NODOS_GEOJSON_PATH, "r", encoding="utf-8") as f:
    NODOS_GEOJSON = json.load(f)

with open(CATALOGO_NODOS_PATH, "r", encoding="utf-8") as f:
    CATALOGO_NODOS = json.load(f)

with open(VERTICES_JSON_PATH, "r", encoding="utf-8") as f:
    VERTICES_LIST = json.load(f)

with open(ATTR_OP_PATH, "r", encoding="utf-8") as f:
    ATTR_OP_DATA = json.load(f)

with open(SISMO_GEOJSON_PATH, "r", encoding="utf-8") as f:
    SISMO_GEOJSON = json.load(f)

with open(ATTR_POST_PATH, "r", encoding="utf-8") as f:
    ATTR_POST_DATA = json.load(f)

EDGES_SIMPLE = [
    {
        "gid": feat["properties"]["gid"],
        "source": feat["properties"]["source"],
        "target": feat["properties"]["target"],
        "prob_falla": float(feat["properties"]["prob_falla"]),
        "es_sintetico": bool(feat["properties"]["es_sintetico"]),
    }
    for feat in RED_GEOJSON["features"]
]

STRATEGIC_KEY_NODES = [n["id_vertice"] for n in CATALOGO_NODOS]
MAIN_BACKBONE_KEY_NODES = [
    v["id"] for v in VERTICES_LIST if v["cnt"] >= 3 and v["componente"] == 1
]
ALL_GLOBAL_KEY_NODES = [v["id"] for v in VERTICES_LIST if v["cnt"] >= 3]


def calcular_attr_subgrafo(surviving_edges, target_nodes):
    """Calcula el ATTR exacto sobre el subgrafo sobreviviente."""
    K = len(target_nodes)
    if K <= 1:
        return 1.0
    total_pairs = K * (K - 1) // 2
    target_set = set(target_nodes)
    adj = defaultdict(list)
    for e in surviving_edges:
        u, v = e["source"], e["target"]
        adj[u].append(v)
        adj[v].append(u)

    seen = set()
    connected_pairs = 0
    for u in target_nodes:
        if u not in seen:
            q = [u]
            seen.add(u)
            k_c = 0
            while q:
                curr = q.pop()
                if curr in target_set:
                    k_c += 1
                for nxt in adj[curr]:
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append(nxt)
            connected_pairs += k_c * (k_c - 1) // 2
    return connected_pairs / total_pairs


def cargar_bd_postgresql():
    """
    Levanta el contenedor Docker PostgreSQL/PostGIS/pgRouting (`ruteo_chile_db`)
    mediante `docker compose up -d` y carga `main.sql`.
    """
    import time

    pgdb = os.environ.get("PGDATABASE", "ruteo_chile")
    pguser = os.environ.get("PGUSER", "postgres")

    inspect = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", "ruteo_chile_db"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if inspect.returncode != 0 or "true" not in inspect.stdout.lower():
        up_res = subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=90,
        )
        if up_res.returncode != 0:
            raise RuntimeError(
                f"No se pudo iniciar Docker Compose. Verifica que Docker Desktop esté abierto.\n{up_res.stderr}"
            )
        for _ in range(25):
            ready = subprocess.run(
                ["docker", "exec", "ruteo_chile_db", "pg_isready", "-U", pguser, "-d", pgdb],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if ready.returncode == 0:
                break
            time.sleep(1.5)

    with open(MAIN_SQL_PATH, "r", encoding="utf-8") as sql_f:
        sql_content = sql_f.read()

    res_docker = subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            "ruteo_chile_db",
            "psql",
            "-U",
            pguser,
            "-d",
            pgdb,
            "-v",
            "ON_ERROR_STOP=1",
            "-q",
        ],
        input=sql_content,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=90,
    )
    if res_docker.returncode != 0:
        raise RuntimeError(f"Error al cargar main.sql en PostgreSQL (Docker):\n{res_docker.stderr}")

    return True, (
        f"Base de datos '{pgdb}' cargada en Docker (contenedor ruteo_chile_db, puerto 5432) con main.sql."
    )


app = FastAPI(
    title="Resiliencia Red Troncal Chile - Terremoto M 8.8 (Leaflet + pgRouting)",
    version="2.0.0",
)


class SimulacionRequest(BaseModel):
    modo: str = "threshold"
    umbral: Optional[float] = 0.25


@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open(HTML_INDEX_PATH, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/red")
def get_red_geojson():
    return JSONResponse(content=RED_GEOJSON)


@app.get("/api/nodos-clave")
def get_nodos_clave():
    return JSONResponse(content=NODOS_GEOJSON)


@app.get("/api/sismo")
def get_sismo_geojson():
    return JSONResponse(content=SISMO_GEOJSON)


@app.get("/api/attr")
def get_attr_metrics():
    return JSONResponse(
        content={
            "operacion": ATTR_OP_DATA,
            "post_sismo": ATTR_POST_DATA,
        }
    )


@app.post("/api/simular")
def simulate_earthquake(req: SimulacionRequest):
    surviving = []
    failed_gids = []

    if req.modo == "montecarlo":
        for e in EDGES_SIMPLE:
            if random.random() < e["prob_falla"]:
                failed_gids.append(e["gid"])
            else:
                surviving.append(e)
    else:
        tau = req.umbral if req.umbral is not None else 0.25
        for e in EDGES_SIMPLE:
            if e["prob_falla"] >= tau:
                failed_gids.append(e["gid"])
            else:
                surviving.append(e)

    attr_strat_before = ATTR_OP_DATA["metricas_attr_operacion"]["nodos_estrategicos_chile_23"]["attr_operacion"]
    attr_backbone_before = 1.0
    attr_global_before = ATTR_OP_DATA["metricas_attr_operacion"]["global_pais_grado_3_mas"]["attr_operacion"]

    attr_strat_after = calcular_attr_subgrafo(surviving, STRATEGIC_KEY_NODES)
    attr_backbone_after = calcular_attr_subgrafo(surviving, MAIN_BACKBONE_KEY_NODES)
    attr_global_after = calcular_attr_subgrafo(surviving, ALL_GLOBAL_KEY_NODES)

    caida_strat_pct = 100.0 * (attr_strat_before - attr_strat_after) / attr_strat_before
    caida_backbone_pct = 100.0 * (attr_backbone_before - attr_backbone_after) / attr_backbone_before
    caida_global_pct = 100.0 * (attr_global_before - attr_global_after) / attr_global_before

    return {
        "modo": req.modo,
        "umbral": req.umbral,
        "cantidad_enlaces_fallados": len(failed_gids),
        "enlaces_fallados_gids": failed_gids,
        "attr_estrategicos_antes": round(attr_strat_before, 6),
        "attr_estrategicos_despues": round(attr_strat_after, 6),
        "caida_estrategicos_pct": round(caida_strat_pct, 2),
        "attr_backbone_antes": round(attr_backbone_before, 6),
        "attr_backbone_despues": round(attr_backbone_after, 6),
        "caida_backbone_pct": round(caida_backbone_pct, 2),
        "attr_global_antes": round(attr_global_before, 6),
        "attr_global_despues": round(attr_global_after, 6),
        "caida_global_pct": round(caida_global_pct, 2),
    }


def imprimir_resumen_completo():
    s23 = ATTR_POST_DATA["nodos_estrategicos_chile"]
    b3 = ATTR_POST_DATA["backbone_principal_grado3"]
    g3 = ATTR_POST_DATA["red_global_grado3"]
    eq_props = SISMO_GEOJSON["features"][0]["properties"]

    print("=" * 88)
    print("  FLUJO COMPLETO TI2: RESILIENCIA DE LA INFRAESTRUCTURA DE INTERNET CHILENA")
    print("  PROYECTO YAFÚN (SUBTEL SAIP Respuesta_T5610) & TERREMOTO M 8.8 DEL MAULE (27F)")
    print("=" * 88)
    print("  [1.0 & 2.0] INFRAESTRUCTURA, TOPOLOGÍA (pgr_createTopology) Y ENLACES SINTÉTICOS:")
    print(f"    * Fibra Óptica Original SAIP (es_sintetico=FALSE) : {ATTR_OP_DATA['enlaces_fibra_original_saip']:4d} tramos ({ATTR_OP_DATA['km_fibra_original_saip']:9.2f} km)")
    print(f"    * Enlaces Sintéticos/Compl.  (es_sintetico=TRUE)  : {ATTR_OP_DATA['enlaces_sinteticos_complementarios']:4d} tramos ({ATTR_OP_DATA['km_sinteticos_complementarios']:9.2f} km)")
    print(f"    * Total Red Troncal (tolerancia = 0.0001°)        : {len(EDGES_SIMPLE):4d} tramos ({ATTR_OP_DATA['longitud_total_km']:9.2f} km) | {len(VERTICES_LIST)} vértices")
    print(f"    * Nodos Clave Estratégicos (CLS, IXP/PIT, DC)     : {len(STRATEGIC_KEY_NODES)} nodos nombrados")
    print(f"    * Nodos Clave Topológicos (Grado >= 3)            : {len(ALL_GLOBAL_KEY_NODES)} nodos (133 en Backbone Centro-Sur)")
    print("-" * 88)
    print("  [3.0 & 3.1] ATTR EN OPERACIÓN (prob_falla = 0 por defecto):")
    print(f"    * 23 Nodos Estratégicos (Solo Fibra 10.316 km)    : ATTR = {ATTR_OP_DATA['metricas_attr_operacion']['nodos_estrategicos_chile_23']['attr_solo_fibra_sin_sinteticos']:.6f} (2.77%)")
    print(f"    * 23 Nodos Estratégicos (Red Completa 27.523 km)  : ATTR = {s23['attr_antes']:.6f} (14.23% - 36/253 pares en 9 subredes)")
    print(f"    * Backbone Principal Conectado (133 nodos g>=3)   : ATTR = {b3['attr_antes']:.6f} (100.00% - 8778/8778 pares)")
    print(f"    * Red Global Nacional (367 nodos g>=3)            : ATTR = {g3['attr_antes']:.6f} (18.51% - 12429/67161 pares)")
    print("-" * 88)
    print("  [4.0 a 4.3] TERREMOTO 8.8 USGS Y PROBABILIDADES DE FALLA (main.sql):")
    print(f"    * Evento USGS : {eq_props['id_evento']} | Mw={eq_props['magnitud']} | Epicentro=({eq_props['latitud']}°, {eq_props['longitud']}°) | h={eq_props['profundidad_km']} km")
    top1 = ATTR_POST_DATA["top10_enlaces_mas_afectados"][0]
    low1 = ATTR_POST_DATA["top10_enlaces_menos_afectados"][0]
    print(f"    * Enlace más afectado   : GID=#{top1['gid']} ({top1['tipo_tramo']}) a {top1['dist_epicentro_km']} km -> PGA={top1['pga_g']}g, P(falla)={top1['prob_falla']:.4f}")
    print(f"    * Enlace menos afectado : GID=#{low1['gid']} ({low1['tipo_tramo']}) a {low1['dist_epicentro_km']} km -> PGA={low1['pga_g']}g, P(falla)={low1['prob_falla']:.6f}")
    print("-" * 88)
    print(f"  [5.0] NUEVO ATTR POST-TERREMOTO M 8.8 (Simulación Monte Carlo, N={ATTR_POST_DATA['iteraciones_monte_carlo']} iteraciones):")
    print(f"    * Enlaces fallados promedio por sismo             : {ATTR_POST_DATA['enlaces_fallados_promedio']} ± {ATTR_POST_DATA['enlaces_fallados_std']} enlaces")
    print(f"    1) 23 Nodos Clave Estratégicos (CLS/IXP/DC)       : Antes = {s23['attr_antes']:.6f} -> Después = {s23['attr_despues_esperado_mc']:.6f} (Dif: -{s23['caida_absoluta']:.6f} | -{s23['caida_porcentual']:.2f}%)")
    print(f"    2) Backbone Principal Conectado (133 nodos g>=3)  : Antes = {b3['attr_antes']:.6f} -> Después = {b3['attr_despues_esperado_mc']:.6f} (Dif: -{b3['caida_absoluta']:.6f} | -{b3['caida_porcentual']:.2f}%)")
    print(f"    3) Red Global Nacional (367 nodos g>=3)           : Antes = {g3['attr_antes']:.6f} -> Después = {g3['attr_despues_esperado_mc']:.6f} (Dif: -{g3['caida_absoluta']:.6f} | -{g3['caida_porcentual']:.2f}%)")
    print("=" * 88)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Flujo unificado TI2: Carga BD (main.sql), calcula probabilidades, ATTR (antes y después) y levanta Leaflet."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host del servidor web (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor web (default: 8000)")
    parser.add_argument("--report-only", action="store_true", help="Ejecutar flujo, mostrar reporte en consola y salir")
    args = parser.parse_args()

    # Intentar cargar main.sql en PostgreSQL automáticamente como parte del flujo único
    ok_db, msg_db = cargar_bd_postgresql()
    imprimir_resumen_completo()
    print(f"  [Estado BD] {msg_db.replace('<code>', '').replace('</code>', '').replace('<strong>', '').replace('</strong>', '')}")

    if args.report_only:
        sys.exit(0)

    print(f"\n  [6.0 & 6.1] Visor interactivo Leaflet disponible en: http://{args.host}:{args.port}\n")
    uvicorn.run(app, host=args.host, port=args.port)
