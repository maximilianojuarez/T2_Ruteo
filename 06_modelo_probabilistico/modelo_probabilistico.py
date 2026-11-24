"""
PUNTO 6: Implementación del Modelo de Falla Probabilístico Sísmico
basado en la Ley de Atenuación de Fukushima & Tanaka (1990) / Contreras & Boroschek (2012)
y Curvas de Fragilidad Lognormal (FEMA HAZUS-MH / Esposito et al., 2015).
"""
import math
from scipy.stats import norm

def calcular_pga_y_probabilidad_falla(dist_epi_km, longitud_km, mw=8.8, depth_km=22.9, theta_pga=0.35, beta_frag=0.45):
    R_hypo = math.sqrt(dist_epi_km ** 2 + depth_km ** 2)
    c_mag = 0.032 * (10.0 ** (0.41 * mw))
    log10_pga_gal = 0.41 * mw - math.log10(R_hypo + c_mag) - 0.0034 * R_hypo + 1.30
    pga_g = (10.0 ** log10_pga_gal) / 980.665
    z = math.log(max(pga_g, 1e-9) / theta_pga) / beta_frag
    p_base = float(norm.cdf(z))
    factor_long = 1.0 + 0.04 * (min(longitud_km, 50.0) / 10.0)
    p_falla = 1.0 - ((1.0 - p_base) ** factor_long)
    return round(pga_g, 4), round(p_falla, 4)

if __name__ == "__main__":
    print("=====================================================================")
    print("  PUNTO 6: CURVA DE ATENUACIÓN (PGA) Y PROBABILIDAD DE FALLA (Mw=8.8)")
    print("=====================================================================")
    print("Dist. Epicentral | PGA (g) | P(Falla Fibra) | P(Falla Postación) | P(Falla Camino)")
    print("-" * 82)
    for d in [10, 25, 50, 100, 150, 200, 300, 500]:
        pga, p_fo = calcular_pga_y_probabilidad_falla(d, 10.0, theta_pga=0.42, beta_frag=0.45)
        _, p_pe = calcular_pga_y_probabilidad_falla(d, 10.0, theta_pga=0.26, beta_frag=0.42)
        _, p_cs = calcular_pga_y_probabilidad_falla(d, 10.0, theta_pga=0.32, beta_frag=0.44)
        print(f"    {d:4d} km      | {pga:6.3f}g |     {p_fo:6.4f}     |       {p_pe:6.4f}       |     {p_cs:6.4f}")
