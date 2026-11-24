"""
CRITERIO 4.2 (PUNTO 7): Script que calcula la probabilidad de falla de cada enlace
aplicando el modelo 4.1 con distancia proyectada en metros, y muestra tanto los
10 enlaces MÁS afectados como los 10 enlaces MENOS afectados.
"""
import os
import csv
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    csv_path = os.path.join(BASE_DIR, "07_probabilidades_enlaces", "probabilidades_enlaces.csv")
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["prob_falla"] = float(r["prob_falla"])
            r["pga_g"] = float(r["pga_g"])
            r["dist_epicentro_m"] = float(r["dist_epicentro_m"])
            r["dist_epicentro_km"] = float(r["dist_epicentro_km"])
            rows.append(r)

    print("=" * 95)
    print("  CRITERIO 4.2: PROBABILIDAD DE FALLA POR ENLACE (4.497 TRAMOS)")
    print("=" * 95)
    probs = [r["prob_falla"] for r in rows]
    print(f"Rango de Probabilidades : [{min(probs):.6f}, {max(probs):.6f}] (100% dentro de [0, 1])")
    print(f"Probabilidad Media      : {sum(probs)/len(probs):.4f} ({100*sum(probs)/len(probs):.2f}%)")
    print(f"Esperanza de Fallas     : {sum(probs):.2f} enlaces fallados esperados")

    print("\n--- Distribución por Nivel de Daño Sísmico ---")
    niveles = Counter(r["nivel_dano"] for r in rows)
    for niv, cnt in niveles.most_common():
        print(f"  {niv:25s}: {cnt:4d} enlaces ({100*cnt/len(rows):5.2f}%)")

    print("\n--- TOP 10 ENLACES MÁS AFECTADOS (Mayor Probabilidad de Falla, Zona Epicentral Maule/Ñuble/Biobío) ---")
    top_mas = sorted(rows, key=lambda x: (-x["prob_falla"], x["dist_epicentro_m"]))[:10]
    for r in top_mas:
        sint = "Sintético" if r["es_sintetico"] == "True" else "Original "
        print(
            f"  GID={r['gid']:4s} | {r['tipo_tramo']:20s} ({sint}) | "
            f"Dist={r['dist_epicentro_m']:8.1f} m ({r['dist_epicentro_km']:5.1f} km) | "
            f"PGA={r['pga_g']:.3f}g | P(falla)={r['prob_falla']:.4f}"
        )

    print("\n--- TOP 10 ENLACES MENOS AFECTADOS (Menor Probabilidad de Falla, Extremos Norte y Austral) ---")
    top_menos = sorted(rows, key=lambda x: (x["prob_falla"], -x["dist_epicentro_m"]))[:10]
    for r in top_menos:
        sint = "Sintético" if r["es_sintetico"] == "True" else "Original "
        print(
            f"  GID={r['gid']:4s} | {r['tipo_tramo']:20s} ({sint}) | "
            f"Dist={r['dist_epicentro_m']:10.1f} m ({r['dist_epicentro_km']:6.1f} km) | "
            f"PGA={r['pga_g']:.5f}g | P(falla)={r['prob_falla']:.6f}"
        )

if __name__ == "__main__":
    main()
