-- =============================================================================
-- PUNTO 1: Carga de la Infraestructura Troncal Chilena (Proyecto Yafún - SUBTEL)
-- Fuente: Solicitud de Transparencia AN002T0005610 (Respuesta_T5610)
-- Capas incluidas (4.497 tramos lineales, 27.523,0 km):
--   1. fibra_optica_detectada.shp          (1.915 tramos - 10.316,0 km)
--   2. postacion_electrica_detectada.shp   (1.213 tramos -  6.711,6 km)
--   3. camino_sin_postacion_detectado.shp  (1.165 tramos -  8.108,4 km)
--   4. trayecto_en_ferry.shp               (  204 tramos -  2.387,1 km)
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgrouting;

-- Comandos shp2pgsql equivalentes para importar directamente desde Respuesta_T5610:
-- shp2pgsql -I -s 4326 info/Respuesta_T5610/fibra_optica_detectada.shp public.capa_fibra_optica | psql -d ruteo_chile
-- shp2pgsql -I -s 4326 info/Respuesta_T5610/postacion_electrica_detectada.shp public.capa_postacion_electrica | psql -d ruteo_chile
-- shp2pgsql -I -s 4326 info/Respuesta_T5610/camino_sin_postacion_detectado.shp public.capa_camino_sin_postacion | psql -d ruteo_chile
-- shp2pgsql -I -s 4326 info/Respuesta_T5610/trayecto_en_ferry.shp public.capa_trayecto_ferry | psql -d ruteo_chile

-- Nota: El archivo ../main.sql en la raíz del proyecto ya incluye los 4.497 INSERTs
-- unificados en la tabla `red_troncal` sin depender de herramientas externas de línea de comandos.
