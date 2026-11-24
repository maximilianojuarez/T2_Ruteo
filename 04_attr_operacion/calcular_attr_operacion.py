"""
CRITERIO 3.0 y 3.1 (PUNTO 4): Calcula el ATTR de la infraestructura en operación
(prob_falla = 0 por defecto) e interpreta el resultado, detallando explícitamente
qué nodos clave quedan conectados entre sí y cuáles quedan en componentes desconectadas.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    res_path = os.path.join(BASE_DIR, "04_attr_operacion", "resultados_attr_operacion.json")
    with open(res_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 95)
    print("  CRITERIOS 3.0 Y 3.1: ATTR DE LA INFRAESTRUCTURA EN OPERACIÓN (PRE-TERREMOTO)")
    print("=" * 95)
    print(f"Fórmula    : ATTR = (2 / (K*(K-1))) * Sum_{{u<v}} P(u <-> v)")
    print(f"Referencia : {data['referencia_bibliografica']}")
    print(f"Fibra SAIP : {data['enlaces_fibra_original_saip']} tramos ({data['km_fibra_original_saip']} km) [es_sintetico = FALSE]")
    print(f"Sintéticos : {data['enlaces_sinteticos_complementarios']} tramos ({data['km_sinteticos_complementarios']} km) [es_sintetico = TRUE]")
    print(f"Total Red  : {data['total_enlaces_topologia']} tramos ({data['longitud_total_km']} km) | {data['total_vertices_topologia']} vértices")
    print("-" * 95)

    for k, m in data["metricas_attr_operacion"].items():
        print(f"[{k}]")
        print(f"  Descripción     : {m['descripcion']}")
        print(f"  Nodos Clave (K) : {m['cantidad_nodos_clave']}")
        print(f"  Pares Conectados: {m['pares_conectados']} / {m['pares_totales']}")
        print(f"  ATTR Operación  : {m['attr_operacion']:.6f} ({m['attr_operacion']*100:.2f}%)")
        if "attr_solo_fibra_sin_sinteticos" in m:
            print(f"  ATTR Solo Fibra : {m['attr_solo_fibra_sin_sinteticos']:.6f} ({m['attr_solo_fibra_sin_sinteticos']*100:.2f}%) [sin enlaces sintéticos]")
        print()

    print("-" * 95)
    print("  INTERPRETACIÓN (CRITERIO 3.1): ¿POR QUÉ ATTR < 1 EN LA RED NACIONAL Y QUÉ NODOS QUEDAN DESCONECTADOS?")
    print("-" * 95)
    print("  En los shapefiles públicos entregados por SUBTEL (Respuesta_T5610), los trazados troncales presentan")
    print("  interrupciones cartográficas en los accesos urbanos a grandes ciudades, dividiendo los 23 Nodos Clave")
    print("  Estratégicos en 9 subredes (componentes conexas) independientes entre sí:")
    for sub in data["desglose_subredes_nodos_estrategicos_operacion"]:
        print(
            f"  * Subred #{sub['subred_id']} ({sub['cantidad_nodos_clave']} nodos clave, "
            f"{sub['pares_internos_conectados']} pares conectados):"
        )
        print(f"      {', '.join(sub['nodos'])}")

if __name__ == "__main__":
    main()
