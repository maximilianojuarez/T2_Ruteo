"""
Genera la figura cartográfica de alta resolución (10_aplicacion_web/captura_mapa_leaflet.png)
con los nodos clave, enlaces originales vs. sintéticos, epicentro M 8.8 y daño por probabilidad
de falla para incluir directamente como evidencia visual en el informe (Criterio 6.1).
"""
import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    with open(os.path.join(BASE_DIR, "01_infraestructura", "red_troncal_chile.geojson"), encoding="utf-8") as f:
        red = json.load(f)
    with open(os.path.join(BASE_DIR, "02_nodos_clave", "catalogo_nodos_estrategicos.json"), encoding="utf-8") as f:
        nodos_est = json.load(f)
    with open(os.path.join(BASE_DIR, "05_terremoto_geojson", "terremoto_8_8_maule.geojson"), encoding="utf-8") as f:
        sismo = json.load(f)

    eq_lon, eq_lat, _ = sismo["features"][0]["geometry"]["coordinates"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 10), facecolor="#0f172a")

    for ax in (ax1, ax2):
        ax.set_facecolor("#0b2239")
        ax.tick_params(colors="#cbd5e1", labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor("#334155")
        ax.grid(True, linestyle=":", alpha=0.25, color="#64748b")

    # Panel 1: Red Nacional por Tipo (Original SAIP continuo vs Sintéticos punteados)
    for feat in red["features"]:
        coords = feat["geometry"]["coordinates"]
        xs, ys = zip(*coords)
        p = feat["properties"]
        ls = "--" if p["es_sintetico"] else "-"
        lw = 0.9 if p["es_sintetico"] else 1.4
        ax1.plot(xs, ys, color=p["color_capa"], linestyle=ls, linewidth=lw, alpha=0.88)

    for n in nodos_est:
        ax1.scatter(n["lon"], n["lat"], s=48, c="#facc15", edgecolors="#7c2d12", linewidths=1.2, zorder=6)
        ax1.text(n["lon"] + 0.35, n["lat"], n["codigo"], color="#f8fafc", fontsize=7, fontweight="bold", zorder=7)

    ax1.scatter(eq_lon, eq_lat, s=150, c="#ef4444", edgecolors="white", linewidths=2.0, zorder=8)
    ax1.set_xlim(-76.5, -66.5)
    ax1.set_ylim(-55.0, -17.5)
    ax1.set_title(
        "A) Red Troncal Chile: Fibra SAIP (continuo) vs. Sintéticos (punteado)\n+ 23 Nodos Clave Estratégicos (CLS / IXP / DC)",
        color="white",
        fontsize=10.5,
        fontweight="bold",
        pad=10,
    )
    ax1.set_xlabel("Longitud (°O)", color="#cbd5e1")
    ax1.set_ylabel("Latitud (°S)", color="#cbd5e1")

    # Panel 2: Zoom Zona Epicentral coloreado por Probabilidad de Falla
    def get_dmg_color(prob):
        if prob >= 0.50:
            return "#ef4444"
        if prob >= 0.25:
            return "#f97316"
        if prob >= 0.10:
            return "#eab308"
        if prob >= 0.02:
            return "#38bdf8"
        return "#10b981"

    for feat in red["features"]:
        coords = feat["geometry"]["coordinates"]
        xs, ys = zip(*coords)
        p = feat["properties"]
        c = get_dmg_color(p["prob_falla"])
        ls = "--" if p["es_sintetico"] else "-"
        lw = 2.0 if p["prob_falla"] >= 0.15 else 1.1
        ax2.plot(xs, ys, color=c, linestyle=ls, linewidth=lw, alpha=0.92)

    for n in nodos_est:
        if -43.0 <= n["lat"] <= -32.5:
            ax2.scatter(n["lon"], n["lat"], s=65, c="#facc15", edgecolors="#000000", linewidths=1.3, zorder=6)
            ax2.text(
                n["lon"] + 0.12,
                n["lat"] + 0.06,
                f"{n['codigo']} ({n['ciudad']})",
                color="#fef08a",
                fontsize=8,
                fontweight="bold",
                zorder=7,
            )

    ax2.scatter(eq_lon, eq_lat, s=200, c="#ef4444", edgecolors="white", linewidths=2.2, zorder=9)
    for r_deg, col in [(0.45, "#ef4444"), (0.90, "#f97316"), (1.80, "#eab308")]:
        circle = mpatches.Circle((eq_lon, eq_lat), r_deg, fill=False, edgecolor=col, linestyle="--", linewidth=1.3, zorder=5)
        ax2.add_patch(circle)

    ax2.set_xlim(-74.8, -69.8)
    ax2.set_ylim(-42.5, -32.5)
    ax2.set_title(
        "B) Mapa de Daño Sísmico (Enlaces por Probabilidad de Falla)\nZoom Zona de Ruptura Terremoto M 8.8 Maule (27F)",
        color="white",
        fontsize=10.5,
        fontweight="bold",
        pad=10,
    )
    ax2.set_xlabel("Longitud (°O)", color="#cbd5e1")
    ax2.set_ylabel("Latitud (°S)", color="#cbd5e1")

    out_path = os.path.join(BASE_DIR, "10_aplicacion_web", "captura_mapa_leaflet.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160, facecolor="#0f172a")
    print(f"Captura generada exitosamente en: {out_path}")

if __name__ == "__main__":
    main()
