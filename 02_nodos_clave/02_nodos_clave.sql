-- =============================================================================
-- PUNTO 2: Identificación de los Nodos Clave de la Infraestructura
-- Criterio: Topológico sobre la tabla de vértices generada por pgr_createTopology
-- =============================================================================

-- Agregar columnas de clasificación topológica a red_troncal_vertices_pgr
ALTER TABLE red_troncal_vertices_pgr ADD COLUMN IF NOT EXISTS es_nodo_clave BOOLEAN DEFAULT FALSE;
ALTER TABLE red_troncal_vertices_pgr ADD COLUMN IF NOT EXISTS es_nodo_core BOOLEAN DEFAULT FALSE;
ALTER TABLE red_troncal_vertices_pgr ADD COLUMN IF NOT EXISTS rol_topologico VARCHAR(100);

-- Actualizar clasificación según el grado de incidencia (cnt) calculado por pgRouting:
--   * cnt >= 4 : Nodo Clave Core (Conmutación e Intercambio Troncal Mayor)
--   * cnt = 3  : Nodo Clave de Bifurcación / Intercambio (Conmutación Troncal)
--   * cnt = 1  : Nodo Terminal / Extremo (Generación/Recepción en borde de red)
--   * cnt = 2  : Nodo de Paso / Continuidad Lineal (Empalme intermedio de shapefile)
UPDATE red_troncal_vertices_pgr
SET es_nodo_clave = (cnt >= 3),
    es_nodo_core  = (cnt >= 4),
    rol_topologico = CASE
        WHEN cnt >= 4 THEN 'Nodo Clave Core (Grado >= 4: Intercambio Mayor)'
        WHEN cnt = 3  THEN 'Nodo Clave de Bifurcacion/Intercambio (Grado = 3)'
        WHEN cnt = 1  THEN 'Nodo Terminal / Extremo (Grado = 1: Borde)'
        ELSE 'Nodo de Paso / Continuidad Lineal (Grado = 2)'
    END;

-- Consulta resumen de distribución de grados:
SELECT cnt AS grado_nodo,
       rol_topologico,
       es_nodo_clave,
       COUNT(*) AS cantidad_nodos
FROM red_troncal_vertices_pgr
GROUP BY cnt, rol_topologico, es_nodo_clave
ORDER BY cnt DESC;
