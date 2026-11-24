# Punto 7: Script que Calcula la Probabilidad de Falla de Cada Enlace

## 1. Cálculo con Geometría Proyectada en Metros (SQL y Python)
Tanto en [main.sql](../main.sql) como en [calcular_probabilidades_enlaces.py](./calcular_probabilidades_enlaces.py), la distancia desde cada enlace `LineString` al epicentro del terremoto M 8.8 se calcula proyectando a metros (**UTM Huso 19 Sur, `EPSG:32719` / esferoide `geography`** en PostGIS) para evitar el error de medir distancias euclidianas en grados:

```sql
UPDATE red_troncal r
SET dist_epicentro_m  = ST_Distance(ST_Transform(r.geom, 32719), ST_Transform(s.geom, 32719)),
    dist_epicentro_km = ST_Distance(r.geom::geography, s.geom::geography) / 1000.0,
    dist_hipocentral_km = SQRT(
        POWER(ST_Distance(r.geom::geography, s.geom::geography) / 1000.0, 2)
        + POWER(s.profundidad_km, 2)
    ),
    pga_g = POWER(
        10.0,
        0.41 * s.magnitud
        - LOG(
            SQRT(POWER(ST_Distance(r.geom::geography, s.geom::geography) / 1000.0, 2) + POWER(s.profundidad_km, 2))
            + 0.032 * POWER(10.0, 0.41 * s.magnitud)
          )
        - 0.0034 * SQRT(POWER(ST_Distance(r.geom::geography, s.geom::geography) / 1000.0, 2) + POWER(s.profundidad_km, 2))
        + 1.30
    ) / 980.665
FROM sismo_88 s;
```

---

## 2. Resultados Estadísticos y Enlaces Más y Menos Afectados

Al ejecutar `python 07_probabilidades_enlaces/calcular_probabilidades_enlaces.py`:
- **Rango de probabilidades**: $[0,000000,\; 0,900400] \subset [0, 1]$.
- **Esperanza matemática de enlaces fallados** ($\sum_{e=1}^{4497} p_e$): **$60,51$ enlaces**.

### A. Top 10 Enlaces MÁS Afectados (Costa de Cobquecura, Dichato, Tomé y Constitución — Zona Epicentral)

| GID | Tipo de Tramo | Clasificación | Nodos (`source ↔ target`) | Distancia al Epicentro (m / km) | PGA ($g$) | **Probabilidad de Falla (`prob_falla`)** |
| :---: | :--- | :---: | :---: | ---: | :---: | :---: |
| **`2817`** | `postacion_electrica` | Sintético | `2279 ↔ 2278` | $8.196,6\text{ m}$ ($8,20\text{ km}$) | $0,443\,g$ | **0,9004 (90,04%)** |
| **`2816`** | `postacion_electrica` | Sintético | `2277 ↔ 2278` | $9.299,6\text{ m}$ ($9,30\text{ km}$) | $0,440\,g$ | **0,8995 (89,95%)** |
| **`2819`** | `postacion_electrica` | Sintético | `2280 ↔ 2281` | $9.180,3\text{ m}$ ($9,18\text{ km}$) | $0,440\,g$ | **0,8994 (89,94%)** |
| **`2818`** | `postacion_electrica` | Sintético | `2279 ↔ 2280` | $9.007,6\text{ m}$ ($9,01\text{ km}$) | $0,441\,g$ | **0,8969 (89,69%)** |
| **`2820`** | `postacion_electrica` | Sintético | `2281 ↔ 2282` | $12.502,9\text{ m}$ ($12,50\text{ km}$) | $0,431\,g$ | **0,8915 (89,15%)** |
| **`2815`** | `postacion_electrica` | Sintético | `2276 ↔ 2277` | $12.069,3\text{ m}$ ($12,07\text{ km}$) | $0,433\,g$ | **0,8908 (89,08%)** |
| **`2814`** | `postacion_electrica` | Sintético | `2275 ↔ 2276` | $13.972,1\text{ m}$ ($13,97\text{ km}$) | $0,427\,g$ | **0,8853 (88,53%)** |
| **`2813`** | `postacion_electrica` | Sintético | `2274 ↔ 2275` | $16.929,2\text{ m}$ ($16,93\text{ km}$) | $0,417\,g$ | **0,8725 (87,25%)** |
| **`2821`** | `postacion_electrica` | Sintético | `2282 ↔ 2283` | $17.812,7\text{ m}$ ($17,81\text{ km}$) | $0,414\,g$ | **0,8692 (86,92%)** |
| **`2812`** | `postacion_electrica` | Sintético | `2273 ↔ 2274` | $18.477,1\text{ m}$ ($18,48\text{ km}$) | $0,412\,g$ | **0,8685 (86,85%)** |

*(Nota: Entre los enlaces de **Fibra Óptica Original SAIP**, los más afectados son los tramos costeros y del valle central de Ñuble/Biobío/Maule a $26\text{–}45\text{ km}$ del epicentro, que alcanzan $\text{PGA} \in [0,32g,\; 0,39g]$ y probabilidades de falla de $0,38\text{ a }0,46$).*

### B. Top 10 Enlaces MENOS Afectados (Extremo Norte en Arica/Parinacota y Extremo Austral en Tierra del Fuego/Cabo de Hornos)

| GID | Tipo de Tramo | Clasificación | Nodos (`source ↔ target`) | Distancia al Epicentro (m / km) | PGA ($g$) | **Probabilidad de Falla (`prob_falla`)** |
| :---: | :--- | :---: | :---: | ---: | :---: | :---: |
| **`3372`** | `camino_sin_postacion` | Sintético | `2651 ↔ 2652` | $3.576.720,4\text{ m}$ ($3.576,7\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`3373`** | `camino_sin_postacion` | Sintético | `2652 ↔ 2653` | $3.575.595,2\text{ m}$ ($3.575,6\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`3370`** | `camino_sin_postacion` | Sintético | `2649 ↔ 2650` | $3.574.991,5\text{ m}$ ($3.575,0\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`3371`** | `camino_sin_postacion` | Sintético | `2650 ↔ 2651` | $3.574.991,5\text{ m}$ ($3.575,0\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`4496`** | `trayecto_en_ferry` | Sintético | `4542 ↔ 4555` | $2.226.480,1\text{ m}$ ($2.226,5\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`1390`** | `fibra_optica` | Original SAIP | `817 ↔ 1317` | $1.976.815,0\text{ m}$ ($1.976,8\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`1389`** | `fibra_optica` | Original SAIP | `1316 ↔ 1317` | $1.975.110,4\text{ m}$ ($1.975,1\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`1914`** | `fibra_optica` | Original SAIP | `1907 ↔ 1908` | $1.896.420,8\text{ m}$ ($1.896,4\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`1915`** | `fibra_optica` | Original SAIP | `1908 ↔ 1909` | $1.895.912,3\text{ m}$ ($1.895,9\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
| **`1388`** | `fibra_optica` | Original SAIP | `1315 ↔ 1316` | $1.971.340,2\text{ m}$ ($1.971,3\text{ km}$) | $0,00000\,g$ | **0,000000 (0,00%)** |
