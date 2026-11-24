"""
CRITERIO 1.0 (PUNTO 2): Identifica y lista los Nodos Clave que generan, intercambian
y reciben información (Aterrizajes de cables submarinos, IXP/PIT, Data Centers, Nodos Troncales),
con su ubicación, rol, justificación con fuente y ubicación exacta en la topología (id_vertice).
"""
import os
import json
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    with open(os.path.join(BASE_DIR, "02_nodos_clave", "catalogo_nodos_estrategicos.json"), "r", encoding="utf-8") as f:
        nodos_est = json.load(f)
    with open(os.path.join(BASE_DIR, "03_topologia", "vertices_pgr.json"), "r", encoding="utf-8") as f:
        vertices = json.load(f)

    print("=" * 105)
    print("  CRITERIO 1.0: CATÁLOGO DE 23 NODOS CLAVE ESTRATÉGICOS DE CHILE (CLS, IXP/PIT, DATA CENTERS, TRONCALES)")
    print("=" * 105)
    print(f"{'Código':8s} | {'Ciudad / Región':28s} | {'Vértice':7s} | {'Grado':5s} | {'Comp':4s} | {'Categoría y Rol (Genera/Intercambia/Recibe)'}")
    print("-" * 105)
    for n in nodos_est:
        ciudad_reg = f"{n['ciudad']} ({n['region'].split('(')[-1].rstrip(')')})"
        print(
            f"{n['codigo']:8s} | {ciudad_reg:28s} | #{n['id_vertice']:6d} |   {n['grado_topologico']:2d}  | #{n['componente_operacion']:3d} | "
            f"{n['categoria']} [{n['rol']}]"
        )
        print(f"         -> Ubicación: ({n['lat']:.4f}°, {n['lon']:.4f}°) | Detalle: {n['detalle_rol']}")
        print(f"         -> Fuente   : {n['fuente']}")

    deg_counts = Counter(v["cnt"] for v in vertices)
    print("\n" + "=" * 105)
    print("  DISTRIBUCIÓN TOPOLÓGICA DE VÉRTICES EN pgr_createTopology (4.556 VÉRTICES)")
    print("=" * 105)
    for deg, count in sorted(deg_counts.items()):
        pct = 100.0 * count / len(vertices)
        print(f"  Grado {deg}: {count:4d} vértices ({pct:5.2f}%)")
    print(f"  Total Nodos Clave Topológicos (Grado >= 3): {sum(c for d, c in deg_counts.items() if d >= 3)} vértices")

if __name__ == "__main__":
    main()
