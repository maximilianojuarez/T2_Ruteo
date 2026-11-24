# Punto 1: Descarga y Consolidación de la Infraestructura Troncal Chilena

## Fuente de Datos
Los datos provienen de la respuesta oficial de la **Subsecretaría de Telecomunicaciones (SUBTEL)** a la Solicitud de Acceso a la Información Pública **AN002T0005610** (*Proyecto Yafún / Estudio y Recomendaciones sobre la Resiliencia de la Infraestructura de la Internet Chilena*, NIC Chile / SUBTEL), ubicada en `../info/Respuesta_T5610/`.

## Selección y Justificación de las Capas Lineales
Tal como se especifica en la leyenda oficial del mapa **Red Troncal - Chile** (Imagen 2 del enunciado), se utilizan exclusivamente las **4 capas de geometría lineal (`LineString`, SRID 4326 - WGS84)**, cuya suma exacta coincide con el total reportado en la leyenda (**4.497 tramos y 27.523,0 km**):

| Capa (`Respuesta_T5610`) | Código Tipo (`tipo_tramo`) | Tramos | Longitud (km) | Color Leyenda |
| :--- | :--- | ---: | ---: | :--- |
| `fibra_optica_detectada.shp` | `fibra_optica` | 1.915 | 10.316,0 km | `#1b9e77` (Verde) |
| `postacion_electrica_detectada.shp` | `postacion_electrica` | 1.213 | 6.711,6 km | `#d95f02` (Naranja) |
| `camino_sin_postacion_detectado.shp` | `camino_sin_postacion` | 1.165 | 8.108,4 km | `#7570b3` (Violeta) |
| `trayecto_en_ferry.shp` | `trayecto_en_ferry` | 204 | 2.387,1 km | `#e7298a` (Magenta) |
| **Total Red Troncal** | **4 capas integradas** | **4.497** | **27.523,1 km** | — |

## Archivos en esta Carpeta
- `red_troncal_chile.geojson`: Archivo GeoJSON consolidado con los 4.497 tramos lineales, sus propiedades topológicas y sísmicas.
- `01_cargar_infraestructura.sql`: Script SQL con la estructura y comandos de importación PostGIS.
