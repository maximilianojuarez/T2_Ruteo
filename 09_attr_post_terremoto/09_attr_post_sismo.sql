-- =============================================================================
-- PUNTO 9: Cálculo del Nuevo ATTR Post-Terremoto 8.8 en PostgreSQL / pgRouting
-- Incluye:
--   A) Consulta determinista por umbral de probabilidad de falla
--   B) Función PL/pgSQL para Simulación de Monte Carlo sobre pgr_connectedComponents
-- =============================================================================

-- A) Comparación directa ATTR Antes vs Después (corte determinista prob_falla >= umbral):
SELECT
    (SELECT attr_operacion FROM v_attr_operacion) AS attr_antes_terremoto,
    (SELECT attr_post_terremoto FROM v_attr_post_terremoto) AS attr_despues_umbral_030;

-- B) Función PL/pgSQL para evaluar una realización de Monte Carlo en vivo usando pgRouting:
CREATE OR REPLACE FUNCTION calcular_attr_monte_carlo_una_iteracion()
RETURNS DOUBLE PRECISION AS $$
DECLARE
    v_attr DOUBLE PRECISION;
BEGIN
    WITH enlaces_sobrevivientes AS (
        SELECT gid AS id, source, target, cost, reverse_cost
        FROM red_troncal
        WHERE random() >= prob_falla
    ),
    comp AS (
        SELECT * FROM pgr_connectedComponents(
            'SELECT gid AS id, source, target, cost, reverse_cost FROM red_troncal WHERE random() >= prob_falla'
        )
    ),
    nodos_clave_total AS (
        SELECT COUNT(*)::double precision AS K_tot
        FROM red_troncal_vertices_pgr
        WHERE es_nodo_clave = TRUE
    ),
    nodos_por_comp AS (
        SELECT c.component, COUNT(*)::double precision AS k_c
        FROM comp c
        JOIN red_troncal_vertices_pgr v ON v.id = c.node
        WHERE v.es_nodo_clave = TRUE
        GROUP BY c.component
    )
    SELECT COALESCE(SUM(k_c * (k_c - 1.0) / 2.0), 0.0) / NULLIF(MAX(t.K_tot) * (MAX(t.K_tot) - 1.0) / 2.0, 0.0)
    INTO v_attr
    FROM nodos_clave_total t
    LEFT JOIN nodos_por_comp nc ON TRUE;

    RETURN v_attr;
END;
$$ LANGUAGE plpgsql;
