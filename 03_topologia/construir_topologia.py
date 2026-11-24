"""
PUNTO 3: Script que verifica la topología generada (equivalente a pgr_createTopology)
sobre los 4.497 enlaces y 4.556 vértices.
"""
import os
import json
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    with open(os.path.join(BASE_DIR, "03_topologia", "vertices_pgr.json"), "r", encoding="utf-8") as f:
        vertices = json.load(f)

    comps = Counter(v["componente"] for v in vertices)
    print("=====================================================================")
    print("  PUNTO 3: TOPOLOGÍA DE RED (pgr_createTopology, tolerancia=0.0001)")
    print("=====================================================================")
    print(f"Total Vértices (red_troncal_vertices_pgr): {len(vertices)}")
    print(f"Total Componentes Conexas                : {len(comps)}")
    print("Top 5 Componentes por cantidad de vértices:")
    for cid, cnt in comps.most_common(5):
        print(f"  Componente #{cid}: {cnt} vértices ({100.0*cnt/len(vertices):.2f}%)")

if __name__ == "__main__":
    main()
