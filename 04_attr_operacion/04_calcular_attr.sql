-- =============================================================================
-- PUNTO 4: Cálculo del ATTR de la Infraestructura en Operación Normal
-- =============================================================================
-- Definición de ATTR (All-Terminal / Average Two-Terminal Reliability):
--   ATTR = (Suma de pares de nodos clave conectados entre sí) / (K * (K - 1) / 2)
-- Utilizando pgr_connectedComponents de pgRouting:

WITH componentes AS (
    SELECT * FROM pgr_connectedComponents(
        'SELECT gid AS id, source, target, cost, reverse_cost FROM red_troncal'
    )
),
nodos_clave_por_componente AS (
    SELECT c.component,
           COUNT(*) AS k_c
    FROM componentes c
    JOIN red_troncal_vertices_pgr v ON v.id = c.node
    WHERE v.es_nodo_clave = TRUE
    GROUP BY c.component
),
resumen_global AS (
    SELECT SUM(k_c) AS total_nodos_clave,
           SUM(k_c * (k_c - 1) / 2.0) AS pares_conectados,
           MAX(k_c) AS nodos_clave_backbone_principal
    FROM nodos_clave_por_componente
)
SELECT total_nodos_clave,
       pares_conectados,
       (total_nodos_clave * (total_nodos_clave - 1) / 2.0) AS pares_totales_global,
       ROUND((pares_conectados / (total_nodos_clave * (total_nodos_clave - 1) / 2.0))::numeric, 6) AS attr_global_pais,
       nodos_clave_backbone_principal,
       (nodos_clave_backbone_principal * (nodos_clave_backbone_principal - 1) / 2.0) AS pares_backbone_principal,
       1.000000 AS attr_backbone_principal
FROM resumen_global;
