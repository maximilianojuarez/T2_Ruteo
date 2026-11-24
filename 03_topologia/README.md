# Punto 3: Conversión a Topología con `pgr_createTopology`, Conectividad y Limitaciones

## 1. Ejecución de `pgr_createTopology` y Columna `prob_falla = 0` por Defecto
En [main.sql](../main.sql) y [03_crear_topologia.sql](./03_crear_topologia.sql), la tabla `red_troncal` se define con la columna `prob_falla_operacion DOUBLE PRECISION NOT NULL DEFAULT 0.0` (y `prob_falla DOUBLE PRECISION NOT NULL DEFAULT 0.0` antes de aplicar el terremoto), ejecutando:

```sql
ALTER TABLE red_troncal ADD COLUMN IF NOT EXISTS prob_falla DOUBLE PRECISION NOT NULL DEFAULT 0.0;
ALTER TABLE red_troncal ADD COLUMN IF NOT EXISTS es_sintetico BOOLEAN NOT NULL DEFAULT FALSE;

SELECT pgr_createTopology(
    'red_troncal',   -- Tabla de enlaces
    0.0001,          -- Tolerancia: 0.0001 grados (~11.1 metros en WGS84 SRID 4326)
    'geom',          -- Geometría LineString
    'gid',           -- ID de enlace
    'source',        -- Columna nodo origen
    'target',        -- Columna nodo destino
    clean := true
);

SELECT pgr_analyzeGraph('red_troncal', 0.0001, 'geom', 'gid', 'source', 'target');
```

### Justificación de la Tolerancia (`0.0001°`)
- Las capas de `Respuesta_T5610` están en coordenadas geográficas **WGS84 (`EPSG:4326`)**, donde $1^\circ \approx 111,1\text{ km}$.
- Una tolerancia de `0.0001°` equivale a **$\approx 11,1\text{ metros}$**: permite unir con precisión los vértices donde un tramo de fibra óptica empalma con un tramo de postación eléctrica, camino o ferry, sin fusionar erróneamente nodos paralelos dentro de una misma ciudad (lo cual ocurriría con tolerancias $\ge 0,01^\circ \approx 1,1\text{ km}$).

---

## 2. Declaración de Limitaciones de los Datos SAIP y Justificación de Enlaces Sintéticos
Al inspeccionar los archivos entregados por SUBTEL en la solicitud de transparencia **SAIP `AN002T0005610` (`Respuesta_T5610`)**, se identifica una limitación fundamental documentada en el propio oficio de SUBTEL:

1. **Fibra Óptica Detectada (`fibra_optica_detectada.shp`)**: Contiene únicamente **1.915 tramos** que suman **10.316,0 km** (frente a los **~28.000 km** reportados en el *Estudio de Resiliencia / Proyecto Yafún* de NIC Chile). Si se construye la topología solo con este archivo, la red queda severamente fragmentada ($\text{ATTR} = 0,027668$, apenas $2,77\%$ entre los 23 nodos estratégicos), pues el shapefile público omite tramos donde la fibra utiliza postación eléctrica, fajas viales sin postación identificada o cruces marítimos/lacustres.
2. **Incorporación y Marcado Explícito de Enlaces Sintéticos / Complementarios (`es_sintetico = TRUE`)**:
   Para reconstruir los **27.523,1 km (~28.000 km)** y los **4.497 tramos** de la leyenda oficial del Estudio Yafún, se integran las otras 3 capas lineales del archivo `Respuesta_T5610`, marcándolas explícitamente en la base de datos (`es_sintetico = TRUE`) y distinguiéndolas con trazo punteado en Leaflet:

| Capa en `Respuesta_T5610` | `tipo_tramo` | `es_sintetico` | Tramos | Longitud (km) | Rol y Justificación |
| :--- | :--- | :---: | ---: | ---: | :--- |
| `fibra_optica_detectada.shp` | `fibra_optica` | **`FALSE`** | 1.915 | **10.316,0 km** | Infraestructura de fibra óptica troncal detectada directamente en el SAIP. |
| `postacion_electrica_detectada.shp` | `postacion_electrica` | **`TRUE`** | 1.213 | **6.711,6 km** | Enlace sintético/complementario sobre postación eléctrica aérea para dar continuidad a rutas donde no se detectó ducto subterráneo. |
| `camino_sin_postacion_detectado.shp` | `camino_sin_postacion` | **`TRUE`** | 1.165 | **8.108,4 km** | Enlace sintético/complementario sobre faja vial para cerrar brechas entre tramos troncales. |
| `trayecto_en_ferry.shp` | `trayecto_en_ferry` | **`TRUE`** | 204 | **2.387,1 km** | Enlace sintético marítimo/lacustre (ferry/cruce submarino austral) para vincular Chiloé, Aysén y Magallanes. |
| **Total Red Troncal** | **4 capas** | — | **4.497** | **27.523,1 km** | Coincidencia exacta con los **4.497 tramos (27.523,0 km)** de la leyenda oficial. |

---

## 3. Revisión de Conectividad (`red_troncal_vertices_pgr`)
- **Total de vértices generados**: **4.556 nodos**.
- **Distribución de grados (`cnt`)**:
  - `cnt = 1` (Nodos terminales/hojas): **539 vértices** ($11,83\%$).
  - `cnt = 2` (Nodos de continuidad lineal): **3.650 vértices** ($80,11\%$).
  - `cnt = 3` (Bifurcación/intercambio): **315 vértices** ($6,91\%$).
  - `cnt = 4` (Conmutación Core): **50 vértices** ($1,10\%$).
  - `cnt = 5` (Conmutación Core Mayor): **2 vértices** ($0,04\%$).
- **Componentes conexas**: Existen **138 componentes conexas** en total. Las 5 macro-componentes principales concentran el **$71,29\%$** de todos los vértices del país:
  1. **Componente #1 (Macrozona Centro-Sur: Curicó a Valdivia)**: $1.387$ vértices ($30,44\%$).
  2. **Componente #2 (Macrozona Norte Grande: Arica a Antofagasta/Calama)**: $535$ vértices ($11,74\%$).
  3. **Componente #3 (Macrozona Sur-Austral: Osorno, Puerto Montt, Chiloé y Coyhaique)**: $476$ vértices ($10,45\%$).
  4. **Componente #4 (Macrozona Magallanes: Punta Arenas y Tierra del Fuego)**: $467$ vértices ($10,25\%$).
  5. **Componente #5 (Macrozona Norte Chico - RM: La Serena a Santiago/Quilicura)**: $383$ vértices ($8,41\%$).
- **Por qué persisten componentes separadas**: En la cartografía pública de `Respuesta_T5610`, los polígonos urbanos de ciertas ciudades (ej. el paso urbano entre Santiago y Rancagua, o entre Valdivia y Osorno) presentan interrupciones de varios kilómetros donde no se dibujaron los enlaces urbanos subterráneos privados.
