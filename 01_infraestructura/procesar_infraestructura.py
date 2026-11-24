"""
PUNTO 1: Script para inspeccionar y resumir las 4 capas lineales de Respuesta_T5610
consolidadas en red_troncal_chile.geojson.
"""
import os
import json
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    geojson_path = os.path.join(BASE_DIR, "01_infraestructura", "red_troncal_chile.geojson")
    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    counts = Counter()
    lengths = defaultdict(float)
    for feat in data["features"]:
        props = feat["properties"]
        capa = props["nombre_capa"]
        counts[capa] += 1
        lengths[capa] += float(props["longitud_km"])

    print("=====================================================================")
    print("  PUNTO 1: INFRAESTRUCTURA RED TRONCAL - CHILE (Respuesta_T5610)")
    print("=====================================================================")
    total_tramos = 0
    total_km = 0.0
    for capa, n in counts.items():
        km = lengths[capa]
        total_tramos += n
        total_km += km
        print(f"  - {capa:26s}: {n:4d} tramos | {km:9.1f} km")
    print("---------------------------------------------------------------------")
    print(f"  TOTAL RED TRONCAL           : {total_tramos:4d} tramos | {total_km:9.1f} km")

if __name__ == "__main__":
    main()
