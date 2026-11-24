-- =============================================================================
-- PUNTO 5: Carga del Sismo M 8.8 del Maule (2010) desde GeoJSON a PostGIS
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS postgis;

DROP TABLE IF EXISTS sismo_88 CASCADE;

CREATE TABLE sismo_88 (
    id_evento VARCHAR(64) PRIMARY KEY,
    magnitud DOUBLE PRECISION NOT NULL,
    profundidad_km DOUBLE PRECISION NOT NULL,
    lugar VARCHAR(255),
    fecha_utc TIMESTAMP WITH TIME ZONE,
    mmi_max DOUBLE PRECISION,
    cdi_max DOUBLE PRECISION,
    geom GEOMETRY(Point, 4326)
);

-- Inserción utilizando ST_GeomFromGeoJSON sobre el objeto geometry del archivo GeoJSON:
INSERT INTO sismo_88 (id_evento, magnitud, profundidad_km, lugar, fecha_utc, mmi_max, cdi_max, geom)
VALUES (
    'official20100227063411530_30',
    8.8,
    22.9,
    '2010 Maule, Chile Earthquake',
    '2010-02-27 06:34:11.530+00',
    8.249,
    9.1,
    ST_Force2D(
        ST_SetSRID(
            ST_GeomFromGeoJSON('{"type":"Point","coordinates":[-72.898,-36.122,22.9]}'),
            4326
        )
    )
);

CREATE INDEX idx_sismo_88_geom ON sismo_88 USING GIST (geom);
