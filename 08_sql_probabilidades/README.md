# Punto 8: Generación de `main.sql` con las Probabilidades de Falla

El archivo **`main.sql`** se encuentra tanto en la **raíz del proyecto (`../main.sql`)** (según lo solicitado en el enunciado) como respaldado en esta carpeta (`./main.sql`).

## Contenido de `main.sql`
1. Habilitación de las extensiones `postgis` y `pgrouting`.
2. Creación y carga de la tabla `sismo_88` con el epicentro del terremoto $M_w = 8,8$.
3. Creación e inserción completa de los **4.497 registros** en la tabla `red_troncal` incluyendo su geometría `LineString (SRID 4326)`, `source`, `target`, `longitud_km`, `dist_epicentro_km`, `pga_g`, `prob_falla` y `nivel_dano`.
4. Ejecución de `pgr_createTopology('red_troncal', 0.0001, 'geom', 'gid', 'source', 'target')` y `pgr_analyzeGraph`.
5. Marcado automático de los **Nodos Clave (`cnt >= 3`)** en `red_troncal_vertices_pgr`.
6. Creación de las vistas `v_attr_operacion` y `v_attr_post_terremoto` utilizando `pgr_connectedComponents`.
