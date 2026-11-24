# Punto 5: Sismo 8.8 en Formato GeoJSON desde USGS y Carga en la BD

## 1. Consulta Oficial USGS e Identificador del Evento
El evento sísmico del **27 de febrero de 2010 ($M_w = 8,8$, Maule, Chile)** se obtuvo mediante la API FDSN Event Web Service del **United States Geological Survey (USGS)**:

- **URL de Consulta USGS**:
  `https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2000-1-1%2000:00:00&endtime=2026-11-18%2023:59:59&maxlatitude=14.605&minlatitude=-58.356&maxlongitude=-24.082&minlongitude=-89.121&minmagnitude=8.8&orderby=magnitude&limit=10`
- **ID Oficial del Evento USGS**: `official20100227063411530_30`
- **Detalle GeoJSON del Evento**: `https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=official20100227063411530_30&format=geojson`
- **Archivo GeoJSON Estandarizado en el Repositorio**: [terremoto_8_8_maule.geojson](./terremoto_8_8_maule.geojson)

---

## 2. Carga en la Base de Datos PostGIS y Tabla `sismo_88` Mostrada
El script [05_cargar_terremoto.sql](./05_cargar_terremoto.sql) (integrado también en [main.sql](../main.sql)) crea y puebla la tabla `sismo_88` utilizando `ST_GeomFromGeoJSON`:

```sql
SELECT id_evento, magnitud, tipo_magnitud, profundidad_km, lugar, fecha_utc,
       mmi_max, cdi_max, ST_AsText(geom) AS geom_wkt
FROM sismo_88;
```

### Resultado de la Tabla `sismo_88` en PostgreSQL / PostGIS:

| `id_evento` | `magnitud` | `tipo_magnitud` | `profundidad_km` | `lugar` | `fecha_utc` | `mmi_max` | `cdi_max` | `geom_wkt` (`SRID 4326`) |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| `official20100227063411530_30` | **8.8** | `mww` | **22.9** | `2010 Maule, Chile Earthquake` | `2010-02-27 06:34:11.53+00` | `8.249` | `9.1` | `POINT(-72.898 -36.122)` |
