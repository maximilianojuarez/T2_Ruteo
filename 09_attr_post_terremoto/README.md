# Punto 9: Nuevo ATTR Post-Terremoto 8.8, Comparación, Contraste con el 27F y Limitaciones

## 1. Comparación Numérica del Nuevo ATTR frente al ATTR Previo (Monte Carlo, $N = 500$)
Al ejecutar `python 09_attr_post_terremoto/calcular_attr_post_sismo.py`, se obtiene un promedio de **$60,68 \pm 5,87$ enlaces cortados** por evento sísmico $M_w = 8,8$, impactando el indicador ATTR en los tres niveles de análisis:

| Escenario de Infraestructura Crítica | Nodos Clave ($|K|$) | **ATTR Previo (Operación)** | **Nuevo ATTR Post-8.8 (MC)** | **Diferencia Absoluta ($\Delta\text{ATTR}$)** | **Caída Porcentual ($\%$)** | Intervalo 5% – 95% |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. 23 Nodos Clave Estratégicos (CLS, IXP/PIT, Data Centers, Troncales)** | **23** | **0,142292 (14,23%)** | **0,091826 (9,18%)** | **$-0,050466$** | **$-35,47\%$** | $[0,0751,\; 0,1304]$ |
| **2. Corredor Troncal Principal Centro-Sur (Grado $\ge 3$, Componente #1)** | **133** | **1,000000 (100,00%)** | **0,409739 (40,97%)** | **$-0,590261$** | **$-59,03\%$** | $[0,2778,\; 0,8689]$ |
| **3. Red Nacional Global Topológica (Grado $\ge 3$, todas las componentes)** | **367** | **0,185063 (18,51%)** | **0,107915 (10,79%)** | **$-0,077148$** | **$-41,69\%$** | $[0,0907,\; 0,1679]$ |

---

## 2. Nodos Clave y Enlaces Más Afectados por el Terremoto M 8.8
Los **7 Nodos Clave Estratégicos** ubicados dentro del corredor troncal Centro-Sur (Subred #1: desde Curicó hasta Valdivia, donde originalmente cada nodo alcanzaba a los otros $6$ nodos clave de su macrozona) sufren las mayores pérdidas de conectividad:

| Código | Nodo Clave Estratégico | Región | Distancia al Epicentro | Nodos Clave Alcanzables Antes | Nodos Clave Alcanzables Después (MC) | **Pérdida de Conectividad ($\%$)** |
| :--- | :--- | :--- | ---: | :---: | :---: | :---: |
| **`CUR-TRN`** | **Curicó** (`#630`) | Maule (VII) | $198,8\text{ km}$ | $6$ | $1,64$ | **$-72,60\%$** |
| **`TAL-TRN`** | **Talca** (`#253`) | Maule (VII) | $136,7\text{ km}$ | $6$ | $1,64$ | **$-72,60\%$** |
| **`ZCO-IXP`** | **Temuco (PIT Temuco)** (`#230`) | La Araucanía (IX) | $291,5\text{ km}$ | $6$ | $2,41$ | **$-59,77\%$** |
| **`ZAL-TRN`** | **Valdivia (REUNA/UACh)** (`#1851`) | Los Ríos (XIV) | $411,7\text{ km}$ | $6$ | $2,41$ | **$-59,77\%$** |
| **`CCP-IXP`** | **Concepción / Talcahuano (PIT)** (`#70`) | Biobío (VIII) | $80,4\text{ km}$ | $6$ | $2,66$ | **$-55,73\%$** |
| **`CHI-TRN`** | **Chillán** (`#636`) | Ñuble (XVI) | $89,7\text{ km}$ | $6$ | $2,74$ | **$-54,40\%$** |
| **`LAG-TRN`** | **Los Ángeles** (`#680`) | Biobío (VIII) | $157,5\text{ km}$ | $6$ | $2,95$ | **$-50,80\%$** |

- **Explicación topológica**: El epicentro (`-36.122°, -72.898°`, costa de Cobquecura) se sitúa exactamente entre **Talca** al norte y **Chillán / Concepción** al sur. Al cortarse los enlaces troncales de fibra óptica y postación eléctrica entre los paralelos $35,5^\circ\text{S}$ y $37,0^\circ\text{S}$, **Curicó y Talca quedan escindidos de Chillán, Concepción, Los Ángeles, Temuco y Valdivia**, perdiendo el $72,6\%$ de su alcance dentro del corredor. Simultáneamente, los enlaces costeros e interiores entre Biobío y La Araucanía se fracturan con frecuencia, aislando a **Temuco y Valdivia** ($-59,8\%$).

---

## 3. Contraste con lo Ocurrido Realmente en el Terremoto del 27F de 2010 (Bibliografía)
Los resultados arrojados por nuestro modelo coinciden estrechamente con los reportes técnicos posteriores al terremoto del 27 de febrero de 2010:

1. **Cortes Físicos en el Corredor Longitudinal (Ruta 5 Sur) y Puentes Colapsados**:
   - Según el reporte de **Kwasinski, A. (2010)** (*TCLEE Report: 2010 Maule, Chile, Earthquake Effects on Telecommunications and Power Infrastructure*, IEEE/ASCE) y el balance oficial de **SUBTEL (2010)**, los cables troncales de fibra óptica que cruzaban adosados a puentes carreteros en la Ruta 5 Sur y rutas costeras (Puente Río Claro, Puente Viejo sobre el Río Biobío, pasos superiores en Talca, Parral y Chillán) sufrieron cortes físicos directos por colapso de tableros y desplazamiento de estribos, dividiendo la red troncal chilena entre el norte y el sur del río Maule/Itata — tal como predice la caída del $59,03\%$ en el ATTR del corredor Centro-Sur.
2. **Alta Vulnerabilidad de la Postación Eléctrica Aérea**:
   - **Kwasinski (2010)** documentó que la mayor tasa de fallas físicas ocurrió en cables de telecomunicaciones tendidos sobre postación eléctrica de distribución debido al colapso de postes y caída de escombros en Concepción, Talcahuano, Constitución y Cauquenes, validando nuestra asignación de una mediana de fragilidad más baja ($\theta = 0,26g$) a la capa `postacion_electrica` (donde nuestro modelo concentra las probabilidades de falla más altas, de $0,75\text{ a }0,90$).
3. **Aislamiento de Prefijos BGP en el Sur de Chile y Resiliencia de Cables Submarinos**:
   - El análisis de ruteo global de Internet realizado por **Cowie, J. / Renesys (2010)** (*"Chilean Earthquake Impact on Internet Routing"*, Dyn/Renesys Blog Técnico, marzo 2010) demostró que mientras los cables submarinos internacionales en **Valparaíso (`VAP-CLS`)** permanecieron operativos tras el sismo, numerosos prefijos IP de las regiones del **Maule, Biobío y La Araucanía (`TAL-TRN`, `CCP-IXP`, `ZCO-IXP`)** quedaron inalcanzables durante las primeras 24 a 72 horas por la partición del backbone terrestre longitudinal.

### Referencias Bibliográficas del Contraste 27F
- **Kwasinski, A. (2010)**. *Telecommunications infrastructure performance during the February 27, 2010, Maule, Chile, earthquake*. Technical Council on Lifeline Earthquake Engineering (TCLEE / ASCE) & IEEE Communications Society Report.
- **SUBTEL (2010)**. *Informe de Diagnóstico y Lecciones Aprendidas en Infraestructura de Telecomunicaciones tras el Terremoto del 27 de Febrero de 2010*. Subsecretaría de Telecomunicaciones, Gobierno de Chile.
- **Cowie, J. (2010)**. *Chilean Earthquake: Further Analysis of Internet Routing Impact*. Renesys / Dyn Research Technical Report.
- **Astroza, M., Ruiz, S., & Astroza, R. (2012)**. *Damage assessment and seismic intensity analysis of the 2010 (Mw 8.8) Maule earthquake*. Earthquake Spectra, 28(S1), S145–S164.

---

## 4. Limitaciones del Modelo Implementado
1. **Fuente Puntual (Epicentro) vs. Plano de Ruptura Finita (~500 km)**:
   - El enunciado solicita un modelo de falla a partir del **epicentro** (`-36.122°, -72.898°`). Aunque la ecuación de Fukushima & Tanaka incluye un término de saturación de campo cercano ($0,032\times 10^{0,41 M_w} \approx 130,2\text{ km}$) que aproxima el tamaño de ruptura, el terremoto del 27F tuvo una ruptura elíptica asimétrica de $\approx 500\text{ km}$ de largo entre **Valparaíso/Pichilemu ($33,5^\circ\text{S}$) y la Península de Arauco ($38,2^\circ\text{S}$)** (**Astroza et al., 2012**). Un modelo de fuente puntual subestima ligeramente el PGA en el extremo norte de la ruptura (O'Higgins/RM sur) respecto de un modelo de falla finita (*ShakeMap* USGS).
2. **Ausencia de Microzonificación Sísmica Local ($V_{s30}$ y Licuefacción)**:
   - El modelo calcula el PGA para una condición de suelo promedio regional, sin incorporar el parámetro $V_{s30}$ (velocidad de ondas de corte en los primeros 30 metros) ni mapas locales de susceptibilidad a licuefacción en cuencas fluviales (como la ribera del río Biobío o suelos blandos de Concepción y Talcahuano).
3. **Dependencia Energética (Agotamiento de Baterías y Grupos Electrógenos)**:
   - Como reportó **SUBTEL (2010)**, una fracción importante de las caídas de servicio tras las primeras 4–8 horas no se debió a rotura física de la fibra óptica, sino al colapso de la red eléctrica del SIC y al agotamiento de los bancos de baterías/combustible en nodos repetidores ópticos. Nuestro modelo evalúa el daño estructural directo e inmediato por sacudida sísmica.
4. **Fragmentación Cartográfica de los Shapefiles Públicos SAIP (`Respuesta_T5610`)**:
   - Como se declaró en el módulo de topología, los shapefiles públicos omiten ciertos tramos urbanos subterráneos que conectan las 9 subredes regionales en condiciones normales, lo que hace que el ATTR nacional base parta en $0,1423$ ($14,23\%$) en lugar de $1,0000$. Por ello se evalúa paralelamente el ATTR sobre el **Corredor Centro-Sur Conectado (Subred #1)**, donde el ATTR parte en $1,0000$ y permite aislar con exactitud el efecto de fragmentación del sismo ($1,0000 \to 0,4097$).
