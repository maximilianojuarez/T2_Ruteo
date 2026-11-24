# Punto 6: Modelo de Falla Probabilístico desde el Epicentro y Respaldo en Literatura

## 1. Papers de Origen del Modelo
El modelo probabilístico implementado acopla dos formulaciones clásicas de la ingeniería sísmica y de confiabilidad de líneas de vida (*lifeline networks*):

1. **Ecuación de Atenuación del Movimiento Fuerte del Suelo (GMPE — *Peak Ground Acceleration*, PGA)**:
   - **Paper original**: **Fukushima, Y., & Tanaka, T. (1990)**. *"A new attenuation relation for peak horizontal acceleration of strong earthquake ground motion in Japan"*. Bulletin of the Seismological Society of America (BSSA), 80(4), 757–783.
   - **Validación para subducción interplaca en Chile (Terremoto del Maule 2010)**: **Contreras, V., & Boroschek, R. (2012)**. *"Strong ground motion attenuation relations for Chilean subduction zone interface earthquakes"*. Proceedings of the 15th World Conference on Earthquake Engineering (15WCEE), Paper N° 3126, Lisboa, Portugal.
2. **Curvas de Fragilidad Sísmica Lognormal y Adaptación a Enlaces de Telecomunicaciones / Fibra Óptica**:
   - **Manual de referencia**: **FEMA (2020)**. *HAZUS-MH 2.1 Earthquake Model Technical Manual*, Capítulo 8 (*Lifeline Systems — Communication & Utility Lifelines*). Federal Emergency Management Agency, Washington, D.C.
   - **Paper de aplicación a redes espaciales e infraestructura lineal**: **Esposito, S., Iervolino, I., d'Onofrio, A., Santo, A., Cavalieri, F., & Franchin, P. (2015)**. *"Simulation-based seismic risk assessment of lifeline networks"*. Reliability Engineering & System Safety, 133, 105–116.
   - **Papers de vulnerabilidad espacial de redes de fibra óptica ante desastres geográficos correlacionados (citados en Boettcher et al., 2018, Ref. [5])**:
     - **Neumayer, S., & Modiano, E. (2011)**. *"Network reliability under random circular cuts"*. In Proc. IEEE GLOBECOM 2011, pp. 1–6 (Referencia `[5]` del paper del curso **Boettcher, Prieto, Restrepo & Pezoa, 2018**).
     - **Neumayer, S., Zussman, G., Cohen, R., & Modiano, E. (2011)**. *"Assessing the vulnerability of the fiber infrastructure to disasters"*. IEEE/ACM Transactions on Networking, 19(6), 1610–1623.

---

## 2. Formulación Matemática Completa y Origen de Cada Parámetro

### A. Cálculo de la Distancia Hipocentral ($R_e$) en Kilómetros a partir de la Distancia Proyectada en Metros
Para cada enlace $e \in E$ con geometría `LineString` y el epicentro del sismo $s$ en `(-72.898°, -36.122°)`:
1. Se calcula la distancia horizontal mínima en metros proyectando en **UTM Zona 19S (`EPSG:32719`)** o sobre el esferoide WGS84 (`geography`):
   $$d_{\text{epi, m}}(e) = \min_{x \in e} \text{ST\_Distance}\!\left(\text{ST\_Transform}(x, 32719),\; \text{ST\_Transform}(s, 32719)\right), \qquad d_{\text{epi}}(e) = \frac{d_{\text{epi, m}}(e)}{1000} \;\text{[km]}$$
2. Incorporando la profundidad focal del hipocentro $h = 22,9\text{ km}$ (reportada por USGS para el evento `official20100227063411530_30`), la distancia hipocentral efectiva es:
   $$R_e = \sqrt{d_{\text{epi}}(e)^2 + h^2} \quad \text{[km]}$$

### B. Ley de Atenuación de Fukushima & Tanaka (1990) para $\text{PGA}(e)$
$$\log_{10}\!\left(\text{PGA}_{\text{gal}}(e)\right) = a \cdot M_w - \log_{10}\!\left(R_e + b \cdot 10^{a \cdot M_w}\right) - c \cdot R_e + d$$

$$\text{PGA}_g(e) = \frac{10^{\log_{10}(\text{PGA}_{\text{gal}}(e))}}{g_0}$$

#### Tabla de Parámetros de la Ley de Atenuación (GMPE):

| Parámetro | Valor | Unidad | Significado Físico | Fuente Exacta |
| :---: | :---: | :---: | :--- | :--- |
| $M_w$ | $8,8$ | Adimensional | Magnitud de momento sísmico del terremoto del Maule 27F | USGS (`official20100227063411530_30`) |
| $h$ | $22,9$ | $\text{km}$ | Profundidad focal del hipocentro | USGS (`official20100227063411530_30`) |
| $a$ | $0,41$ | $\text{mag}^{-1}$ | Coeficiente de escalamiento logarítmico por magnitud | Fukushima & Tanaka (1990), Ec. (5), Tabla 2 |
| $b$ | $0,032$ | $\text{km}$ | Factor de saturación de campo cercano ($b \cdot 10^{0,41 M_w} = 130,2\text{ km}$ para $M_w=8,8$) que modela la extensión finita de la fuente de subducción | Fukushima & Tanaka (1990), Ec. (5), p. 768 |
| $c$ | $0,0034$ | $\text{km}^{-1}$ | Coeficiente de amortiguamiento anelástico de la corteza | Fukushima & Tanaka (1990), Ec. (5) |
| $d$ | $1,30$ | $\log_{10}(\text{cm/s}^2)$ | Término constante de calibración para suelo promedio | Fukushima & Tanaka (1990), Ec. (5) / Contreras & Boroschek (2012) |
| $g_0$ | $980,665$ | $\text{cm/s}^2$ | Aceleración de gravedad estándar para convertir $\text{Gal}$ ($\text{cm/s}^2$) a fracciones de $g$ | Constante física estándar SI |

### C. Curva de Fragilidad Lognormal y Adaptación a Enlaces de Fibra y Soportes Complementarios
Siguiendo **FEMA HAZUS-MH** y **Esposito et al. (2015)**, la probabilidad base de que un tramo experimente daño severo/corte dado un nivel de aceleración $\text{PGA}_g(e)$ está dada por la distribución normal estándar acumulada $\Phi(\cdot)$:

$$P_{\text{base}}(\text{Falla}_e \mid \text{PGA}_g(e)) = \Phi\!\left(\frac{\ln\!\left(\text{PGA}_g(e) / \theta_{\text{tipo}}\right)}{\beta_{\text{tipo}}}\right)$$

Dado que un enlace de fibra óptica es un elemento lineal extenso de longitud $L_e$ (en km) compuesto por múltiples vanos, empalmes y cruces de puentes en serie, la probabilidad de supervivencia del enlace decrece con su longitud expuesta (**Esposito et al., 2015; Neumayer et al., 2011**):

$$p_e = 1 - \left(1 - P_{\text{base}}(\text{Falla}_e \mid \text{PGA}_g(e))\right)^{1 + \alpha_L \frac{\min(L_e,\; L_{\max})}{10\text{ km}}}$$

con coeficiente de exposición longitudinal $\alpha_L = 0,04$ por cada $10\text{ km}$ de trazado (acotado en $L_{\max} = 50\text{ km}$ para evitar saturación artificial en enlaces marítimos o interregionales sin nodos intermedios).

#### Tabla de Parámetros de Fragilidad Adaptados por Tipo de Enlace:

| Tipo de Enlace (`tipo_tramo`) | Mediana $\theta_{\text{tipo}}$ ($g$) | Dispersión $\beta_{\text{tipo}}$ | Justificación de la Adaptación a Fibra Óptica y Soportes |
| :--- | :---: | :---: | :--- |
| **`fibra_optica`** (*Original SAIP*) | **$0,42\,g$** | **$0,45$** | Los cables de fibra óptica troncales canalizados bajo tierra presentan alta ductilidad intrínseca, fallando principalmente ante deformación permanente del suelo, licuefacción o colapso de estribos de puentes viales (FEMA HAZUS-MH, estados de daño moderado-extenso en ductos enterrados: $\theta \in [0,35g, 0,50g]$). |
| **`postacion_electrica`** (*Sintético*) | **$0,26\,g$** | **$0,42$** | La fibra óptica desplegada de forma aérea sobre postación eléctrica de distribución/subtransmisión es significativamente más vulnerable debido al vuelco de postes de hormigón/madera, caída de transformadores y latigueo de cables (FEMA HAZUS-MH Electric Power Distribution lines: $\theta \approx 0,25g$). |
| **`camino_sin_postacion`** (*Sintético*) | **$0,32\,g$** | **$0,44$** | Trazados superficiales adosados a fajas de caminos rurales/secundarios sin canalización profunda, expuestos a derrumbes de taludes y asentamientos de terraplén (FEMA HAZUS-MH Highway Roadways). |
| **`trayecto_en_ferry`** (*Sintético*) | **$0,35\,g$** | **$0,48$** | La vulnerabilidad de estos enlaces reside en las rampas portuarias de atraque, terminales costeras y cámaras de empalme de playa expuestas a sacudida costera y tsunami (FEMA HAZUS-MH Ferry & Port Facilities). |
