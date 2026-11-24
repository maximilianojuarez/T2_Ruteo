"""
CRITERIO 5.0 (PUNTO 9): Indica el nuevo ATTR de la infraestructura crítica tras el
terremoto M 8.8 y lo compara con el previo (diferencia absoluta y %), detallando los
enlaces y nodos clave más afectados, el contraste con lo ocurrido en el 27F real y las limitaciones.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    res_path = os.path.join(BASE_DIR, "09_attr_post_terremoto", "resultados_attr_post_sismo.json")
    with open(res_path, "r", encoding="utf-8") as f:
        mc = json.load(f)

    print("=" * 95)
    print("  CRITERIO 5.0: NUEVO ATTR POST-TERREMOTO M 8.8 Y COMPARACIÓN CON EL PREVIO")
    print("=" * 95)
    print(f"Método                     : Simulación de Monte Carlo ({mc['iteraciones_monte_carlo']} iteraciones)")
    print(f"Justificación de N         : {mc['justificacion_iteraciones']}")
    print(f"Enlaces Fallados Promedio  : {mc['enlaces_fallados_promedio']} ± {mc['enlaces_fallados_std']} enlaces")

    e23 = mc["nodos_estrategicos_chile"]
    print("\n1) 23 NODOS CLAVE ESTRATÉGICOS (CLS, IXP/PIT, Data Centers, Nodos Troncales):")
    print(f"   - ATTR Previo (Operación)     : {e23['attr_antes']:.6f} ({e23['attr_antes']*100:.2f}%)")
    print(f"   - Nuevo ATTR Post-Sismo (MC)  : {e23['attr_despues_esperado_mc']:.6f} ({e23['attr_despues_esperado_mc']*100:.2f}%)")
    print(f"   - Diferencia Absoluta         : -{e23['caida_absoluta']:.6f}")
    print(f"   - Reducción Porcentual        : -{e23['caida_porcentual']:.2f}%")

    b3 = mc["backbone_principal_grado3"]
    print("\n2) CORREDOR TRONCAL PRINCIPAL CONECTADO (133 Nodos Clave Topológicos, Grado >= 3):")
    print(f"   - ATTR Previo (Operación)     : {b3['attr_antes']:.6f} (100.00%)")
    print(f"   - Nuevo ATTR Post-Sismo (MC)  : {b3['attr_despues_esperado_mc']:.6f} ({b3['attr_despues_esperado_mc']*100:.2f}%)")
    print(f"   - Diferencia Absoluta         : -{b3['caida_absoluta']:.6f}")
    print(f"   - Reducción Porcentual        : -{b3['caida_porcentual']:.2f}%")

    g3 = mc["red_global_grado3"]
    print("\n3) RED GLOBAL NACIONAL (367 Nodos Clave Topológicos, Grado >= 3):")
    print(f"   - ATTR Previo (Operación)     : {g3['attr_antes']:.6f} ({g3['attr_antes']*100:.2f}%)")
    print(f"   - Nuevo ATTR Post-Sismo (MC)  : {g3['attr_despues_esperado_mc']:.6f} ({g3['attr_despues_esperado_mc']*100:.2f}%)")
    print(f"   - Diferencia Absoluta         : -{g3['caida_absoluta']:.6f}")
    print(f"   - Reducción Porcentual        : -{g3['caida_porcentual']:.2f}%")

    print("\n--- NODOS CLAVE ESTRATÉGICOS MÁS AFECTADOS POR EL TERREMOTO M 8.8 ---")
    afectados = [n for n in mc["impacto_por_nodo_estrategico"] if n["perdida_conectividad_pct"] > 0]
    afectados.sort(key=lambda x: -x["perdida_conectividad_pct"])
    for n in afectados:
        print(
            f"  * {n['codigo']:8s} | {n['ciudad']:12s} ({n['region']:18s}) | Dist. Epicentro: {n['dist_epicentro_km']:5.1f} km | "
            f"Pares alcanzables: {n['nodos_clave_alcanzables_antes']} -> {n['nodos_clave_alcanzables_despues_mc']:.2f} "
            f"(-{n['perdida_conectividad_pct']:.2f}%)"
        )

if __name__ == "__main__":
    main()
