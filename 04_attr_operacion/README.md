# Punto 4: Script y Cálculo del ATTR en Operación

## 1. Definición Formal del ATTR y Referencia Bibliográfica
Siguiendo directamente la formulación del paper del curso de **Boettcher, N., Prieto, Y., Restrepo, S. E., & Pezoa, J. E. (2018)** (*"Resilient Multiculture Network Design in the Presence of Exploit-Triggered Correlated Failures"*, IEEE Latin America Transactions, Vol. 16, No. 9, pp. 2336–2344, **Ecuación (8), p. 2340**) y **Rai & Agrawal (1990)**, la **Fiabilidad Promedio de Dos Terminales (*Average Two-Terminal Reliability*, ATTR)** tras un evento de falla se define como:

$$\text{ATTR} = \binom{|K|}{2}^{-1} \sum_{\substack{i, j \in K \\ i \neq j}} Z_{ij} = \frac{2}{|K|(|K| - 1)} \sum_{u \in K} \sum_{v \in K, v > u} \mathbb{E}\!\left[Z_{uv}\right]$$

donde:
- $K$ es el conjunto de nodos clave de la red ($n = |K|$),
- $\binom{|K|}{2} = \frac{|K|(|K|-1)}{2}$ es el coeficiente binomial (total de pares no ordenados de nodos clave), y
- $Z_{ij} \in \{0, 1\}$ es la variable indicatriz binaria que toma el valor $1$ si existe al menos un camino operativo entre los nodos $i$ y $j$ en el grafo resultante tras la falla, y $0$ en caso contrario.

Para un estado determinista o una realización muestral $G^{(m)}$ cuyas componentes conexas son $\mathcal{C}(G^{(m)})$ (obtenidas en PostGIS/pgRouting mediante `pgr_connectedComponents`), si $K_c = K \cap V(c)$ es el subconjunto de nodos clave en la componente $c \in \mathcal{C}(G^{(m)})$, el número de pares con $Z_{ij} = 1$ dentro de $c$ es $\binom{|K_c|}{2} = \frac{|K_c|(|K_c|-1)}{2}$, por lo que:

$$\text{ATTR}(G^{(m)}, K) = \frac{\sum_{c \in \mathcal{C}(G^{(m)})} |K_c|(|K_c| - 1)}{|K|(|K| - 1)}$$

- **En operación normal (antes del terremoto)**: Como la probabilidad de falla de cada enlace es $p_e = 0$ por defecto, el grafo es determinista y la evaluación es **exacta** en una sola pasada de `pgr_connectedComponents`.
- **Con probabilidades de falla $p_e \in (0, 1)$ (post-terremoto)**: Siguiendo la metodología de simulación estocástica empleada en **Boettcher et al. (2018, Sección VI, p. 2340)**, el script estima $\overline{\text{ATTR}} \pm \sigma$ mediante **Simulación de Monte Carlo** con $N = 500$ realizaciones independientes. Con $N = 500$ y $\sigma_{\text{ATTR}} \le 0,10$, el error estándar de la media es $\text{SE} = \sigma / \sqrt{N} \le 0,0045$ ($< 0,45\%$), logrando un intervalo de confianza al $95\%$ de semiamplitud inferior a $\pm 0,009$.

### Referencias Bibliográficas del Método ATTR
1. **Boettcher, N., Prieto, Y., Restrepo, S. E., & Pezoa, J. E. (2018)**. *Resilient Multiculture Network Design in the Presence of Exploit-Triggered Correlated Failures*. IEEE Latin America Transactions, Vol. 16, No. 9, pp. 2336–2344 (Ecuación 8, p. 2340).
2. **Rai, S., & Agrawal, D. P. (1990)**. *Distributed computing network reliability*. IEEE Computer Society Press (Referencia [21] en Boettcher et al., 2018).
3. **Ball, M. O. (1986)**. *Computational complexity of network reliability analysis: An overview*. IEEE Transactions on Reliability, 35(3), 230–239.
4. **Sterbenz, J. P., Hutchison, D., Çetinkaya, E. K., Jabbar, A., Rohrer, J. P., Schöller, M., & Smith, P. (2014)**. *Redundancy, diversity, and connectivity to achieve multilevel network resilience, survivability, and disruption tolerance*. Telecommunication Systems, 56(1), 17–31 (Referencia [8] en Boettcher et al., 2018).

---

## 2. Valor del ATTR en Operación e Interpretación de Nodos Desconectados

Al ejecutar `python 04_attr_operacion/calcular_attr_operacion.py`:

| Conjunto de Nodos Clave Evaluado | Nodos ($|K|$) | Pares Conectados | Pares Totales | **ATTR en Operación** |
| :--- | :---: | :---: | :---: | :---: |
| **1. 23 Nodos Clave Estratégicos (Solo Fibra SAIP, 10.316 km, sin sintéticos)** | 23 | 7 | 253 | **0,027668 (2,77%)** |
| **2. 23 Nodos Clave Estratégicos (Red Completa 27.523 km, con sintéticos)** | 23 | 36 | 253 | **0,142292 (14,23%)** |
| **3. Corredor Troncal Centro-Sur Conectado (Grado $\ge 3$, Componente #1)** | 133 | 8.778 | 8.778 | **1,000000 (100,00%)** |
| **4. Red Nacional Global Topológica (Grado $\ge 3$, todas las componentes)** | 367 | 12.429 | 67.161 | **0,185063 (18,51%)** |

### Interpretación: ¿Por qué $\text{ATTR}_{\text{operación}} < 1$ a nivel nacional y qué nodos clave quedan desconectados entre sí?
En los shapefiles públicos de `Respuesta_T5610`, incluso tras incorporar los enlaces complementarios de postación, camino y ferry (lo que multiplica por $5,1\times$ la conectividad respecto de usar solo fibra óptica SAIP, subiendo el ATTR de $0,0277$ a $0,1423$), persisten brechas cartográficas en los anillos metropolitanos donde SUBTEL no publicó los ductos urbanos privados. Como consecuencia, los **23 Nodos Clave Estratégicos** quedan repartidos en **9 subredes (componentes conexas)** mutuamente desconectadas en operación inicial:

1. **Subred #1 — Macrozona Centro-Sur (7 nodos clave conectados entre sí = 21 pares)**:
   - `CUR-TRN` (Curicó, `#630`), `TAL-TRN` (Talca, `#253`), `CHI-TRN` (Chillán, `#636`), `CCP-IXP` (Concepción, `#70`), `LAG-TRN` (Los Ángeles, `#680`), `ZCO-IXP` (Temuco, `#230`) y `ZAL-TRN` (Valdivia, `#1851`).
   - *Nota*: Esta es la componente más grande del país ($1.387$ vértices y $133$ nodos clave de grado $\ge 3$, con $\text{ATTR}_{\text{interno}} = 1,0000$), y se ubica exactamente sobre el área epicentral del terremoto $M_w = 8,8$.
2. **Subred #2 — Macrozona Norte Grande (4 nodos clave conectados entre sí = 6 pares)**:
   - `ARI-CLS` (Arica, `#817`), `IQQ-TRN` (Iquique, `#826`), `ANF-IXP` (Antofagasta, `#24`) y `CJC-TRN` (Calama, `#189`). Desconectada del Norte Chico por una brecha cartográfica al sur de Taltal.
3. **Subred #3 — Macrozona Sur-Austral (4 nodos clave conectados entre sí = 6 pares)**:
   - `ZOS-TRN` (Osorno, `#659`), `PMC-CLS` (Puerto Montt, `#661`), `CCH-CLS` (Castro/Chiloé, `#667`) y `GXQ-TRN` (Coyhaique, `#64`). Vinculada internamente gracias a los enlaces de ferry del Canal de Chacao y rutas australes, pero separada de Valdivia por una brecha en el límite regional Los Ríos / Los Lagos.
4. **Subred #4 — Macrozona Norte Chico y RM (3 nodos clave conectados entre sí = 3 pares)**:
   - `LSC-DC` (La Serena, `#574`), `SCL-IXP` (Santiago Centro, `#374`) y `SCL-DC` (Quilicura Data Centers, `#96`).
5. **Subredes #5 a #9 — Nodos en islas regionales individuales (0 pares entre nodos estratégicos, aunque conectados a sus redes regionales locales)**:
   - `CPO-TRN` (Copiapó, Subred de $167$ vértices en Atacama), `AND-INT` (Los Andes, Subred de $84$ vértices en Aconcagua), `RCG-TRN` (Rancagua, Subred de $61$ vértices en O'Higgins), `VAP-CLS` (Valparaíso, Subred costera de $38$ vértices) y `PUQ-CLS` (Punta Arenas, Subred de Magallanes de $467$ vértices que no cuenta con el tramo submarino oceánico de FOA en el shapefile terrestre).
