-- =============================================================================
-- PUNTO 3: Conversión de la Infraestructura a Topología de Red con pgRouting
-- =============================================================================

-- Asegurar columnas requeridas por pgr_createTopology
ALTER TABLE red_troncal ADD COLUMN IF NOT EXISTS source INTEGER;
ALTER TABLE red_troncal ADD COLUMN IF NOT EXISTS target INTEGER;
ALTER TABLE red_troncal ADD COLUMN IF NOT EXISTS cost DOUBLE PRECISION;
ALTER TABLE red_troncal ADD COLUMN IF NOT EXISTS reverse_cost DOUBLE PRECISION;

-- Calcular costo igual a la longitud geodésica en kilómetros
UPDATE red_troncal
SET longitud_km = ST_Length(geom::geography) / 1000.0,
    cost = ST_Length(geom::geography) / 1000.0,
    reverse_cost = ST_Length(geom::geography) / 1000.0;

-- Construir la topología con tolerancia de 0.0001 grados (~11.1 metros en WGS84)
SELECT pgr_createTopology(
    'red_troncal',   -- Tabla de aristas
    0.0001,          -- Tolerancia en grados (SRID 4326)
    'geom',          -- Columna de geometría
    'gid',           -- Clave primaria de aristas
    'source',        -- Columna nodo origen
    'target',        -- Columna nodo destino
    clean := true    -- Reconstruir limpiamente
);

-- Analizar el grafo para poblar el grado nodal (cnt) en red_troncal_vertices_pgr
SELECT pgr_analyzeGraph(
    'red_troncal',
    0.0001,
    'geom',
    'gid',
    'source',
    'target'
);
