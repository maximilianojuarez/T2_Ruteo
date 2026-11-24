"""
PUNTO 5: Script que transforma info/terremotos.json en un GeoJSON estandarizado
(terremoto_8_8_maule.geojson) listo para ser cargado en PostGIS.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    in_path = os.path.join(BASE_DIR, "info", "terremotos.json")
    out_path = os.path.join(BASE_DIR, "05_terremoto_geojson", "terremoto_8_8_maule.geojson")
    with open(in_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    feat = raw["features"][0]
    lon, lat, depth = feat["geometry"]["coordinates"]
    print("=====================================================================")
    print("  PUNTO 5: GEOJSON DEL SISMO M 8.8 DEL MAULE (USGS)")
    print("=====================================================================")
    print(f"Evento      : {feat['properties']['title']}")
    print(f"ID USGS     : {feat['id']}")
    print(f"Magnitud    : {feat['properties']['mag']} ({feat['properties']['magType']})")
    print(f"Epicentro   : Lat {lat}°, Lon {lon}°")
    print(f"Profundidad : {depth} km")
    print(f"GeoJSON     : {out_path}")

if __name__ == "__main__":
    main()
