# Punto 2: Identificación de Nodos Clave que Generan, Intercambian y Reciben Información

## 1. Fundamentación y Fuentes del Criterio
Siguiendo el *Estudio y Recomendaciones sobre la Resiliencia de la Infraestructura de la Internet Chilena* (**NIC Chile / SUBTEL - Proyecto Yafún, 2018**), la topología oficial de **PIT Chile / NAP Chile** y el registro internacional de cables submarinos (**TeleGeography Submarine Cable Map / Proyecto Fibra Óptica Austral FOA de SUBTEL**), la jerarquía de intercambio de información en Chile se estructura en torno a **cuatro categorías funcionales de nodos clave**:

1. **Estaciones de Aterrizaje de Cables Submarinos (*Cable Landing Stations*, CLS)**: Puertas de enlace internacional y austral que **generan e intercambian** tráfico transoceánico (Arica, Valparaíso/Concón, Puerto Montt, Castro/Quellón, Puerto Chacabuco/Coyhaique y Punta Arenas).
2. **Puntos de Intercambio de Tráfico (*IXP / PIT*)**: Nodos neutros donde los Sistemas Autónomos (ASN), ISPs y CDNs **intercambian** tráfico nacional (Santiago NAP/PIT, PIT Concepción, PIT Temuco, PIT Puerto Montt).
3. **Clústeres de Data Centers (*Hyperscale & Edge Data Centers*)**: Polos que **generan, almacenan y reciben** grandes volúmenes de contenido y servicios cloud (Santiago Norte/Quilicura, Santiago Centro, Antofagasta, Concepción, La Serena/REUNA).
4. **Nodos Troncales Regionales y Pasos Fronterizos Terrestres**: Cabeceras regionales y cruces transandinos (Los Andes, Osorno, Calama) que **agregan, conmutan, intercambian y distribuyen** el tráfico a lo largo del corredor longitudinal chileno.

---

## 2. Catálogo Completo de los 23 Nodos Clave Estratégicos y su Ubicación en la Topología (`red_troncal_vertices_pgr`)

Cada nodo clave ha sido georreferenciado y asociado a su vértice exacto (`id_vertice`) generado por `pgr_createTopology('red_troncal', 0.0001, 'geom', 'gid')`:

| Código | Nombre y Ciudad / Región | Coordenadas (`Lat, Lon`) | ID Vértice (`pgr`) | Grado (`cnt`) | Subred Op. | Categoría y Rol (`Genera / Intercambia / Recibe`) | Fuente |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **`ARI-CLS`** | **Arica** (XV) | `-18.478°, -70.304°` | `#817` | 3 | `#2` | **Aterrizaje Cable Submarino / Frontera** (*Genera / Intercambia / Recibe*): Cable SPSC/Mistral y frontera Perú/Bolivia | SUBTEL / TeleGeography / Yafún |
| **`IQQ-TRN`** | **Iquique** (I) | `-20.258°, -70.129°` | `#826` | 3 | `#2` | **Nodo Troncal Regional** (*Genera / Intercambia / Recibe*): Agregación costera y minera Tarapacá | Estudio Yafún NIC Chile / SUBTEL |
| **`ANF-IXP`** | **Antofagasta** (II) | `-23.647°, -70.395°` | `#24` | 3 | `#2` | **Nodo Troncal / Data Center** (*Genera / Intercambia / Recibe*): Concentrador Norte Grande y Data Centers mineros | SUBTEL / Estudio Yafún |
| **`CJC-TRN`** | **Calama** (II) | `-22.462°, -68.927°` | `#189` | 3 | `#2` | **Nodo Troncal Interior** (*Genera / Intercambia / Recibe*): Conmutación interior y salida Paso Jama | Estudio Yafún NIC Chile / SUBTEL |
| **`CPO-TRN`** | **Copiapó** (III) | `-27.367°, -70.332°` | `#1632` | 3 | `#6` | **Nodo Troncal Regional** (*Genera / Intercambia / Recibe*): Regeneración y agregación Atacama | Estudio Yafún NIC Chile / SUBTEL |
| **`LSC-DC`** | **La Serena / Coquimbo** (IV) | `-29.903°, -71.252°` | `#574` | 3 | `#5` | **Nodo Troncal / Científico** (*Genera / Intercambia / Recibe*): Tráfico astronómico (AURA/ESO/REUNA) y Norte Chico | REUNA / SUBTEL / Estudio Yafún |
| **`VAP-CLS`** | **Valparaíso / Concón** (V) | `-33.033°, -71.603°` | `#608` | 3 | `#10` | **Aterrizaje Cable Submarino Principal** (*Genera / Intercambia / Recibe*): Cables Curie (Google), SAC, PanAm, SAm-1, Mistral y Humboldt | TeleGeography / SUBTEL / Yafún |
| **`AND-INT`** | **Los Andes** (V) | `-32.833°, -70.598°` | `#192` | 3 | `#8` | **Nodo Fronterizo Terrestre** (*Intercambia / Recibe / Genera*): Cruce internacional Los Libertadores hacia Argentina/Atlántico | SUBTEL / Estudio Yafún |
| **`SCL-IXP`** | **Santiago Centro (NAP/PIT)** (RM) | `-33.437°, -70.567°` | `#374` | 3 | `#5` | **IXP / PIT / Core Nacional** (*Genera / Intercambia / Recibe*): NAP Chile y PIT Santiago (interconexión nacional de ISPs y CDNs) | PIT Chile / NAP Chile / SUBTEL |
| **`SCL-DC`** | **Quilicura (Santiago Norte)** (RM) | `-33.309°, -70.690°` | `#96` | 3 | `#5` | **Clúster Data Centers Hyperscale** (*Genera / Intercambia / Recibe*): Google Cloud, AWS, Azure, Equinix, Ascenty, Scala, SONDA, Gtd | Chile Data Centers / SUBTEL |
| **`RCG-TRN`** | **Rancagua** (VI) | `-34.168°, -70.743°` | `#614` | 3 | `#9` | **Nodo Troncal Regional** (*Genera / Intercambia / Recibe*): Conmutación longitudinal O'Higgins | Estudio Yafún NIC Chile / SUBTEL |
| **`CUR-TRN`** | **Curicó** (VII) | `-34.978°, -71.216°` | `#630` | 3 | `#1` | **Nodo Troncal de Bifurcación** (*Intercambia / Recibe / Genera*): Bifurcación longitudinal Ruta 5 Sur y costa Maule | Estudio Yafún NIC Chile / SUBTEL |
| **`TAL-TRN`** | **Talca** (VII) | `-35.432°, -71.648°` | `#253` | 3 | `#1` | **Nodo Troncal Regional** (*Genera / Intercambia / Recibe*): Cabecera óptica Región del Maule (zona ruptura 27F) | Estudio Yafún NIC Chile / SUBTEL |
| **`CHI-TRN`** | **Chillán** (XVI) | `-36.606°, -72.103°` | `#636` | 3 | `#1` | **Nodo Troncal / Bifurcación Crítica** (*Genera / Intercambia / Recibe*): Empalme Ruta 5 Sur con acceso a Concepción (Ruta del Itata) | Estudio Yafún NIC Chile / SUBTEL |
| **`CCP-IXP`** | **Concepción / Talcahuano** (VIII) | `-36.835°, -73.044°` | `#70` | 4 | `#1` | **IXP / PIT Regional / Data Center** (*Genera / Intercambia / Recibe*): PIT Concepción, Data Centers Biobío y nodo costero epicentral | PIT Chile / SUBTEL / Estudio Yafún |
| **`LAG-TRN`** | **Los Ángeles** (VIII) | `-37.470°, -72.351°` | `#680` | 4 | `#1` | **Nodo Troncal Longitudinal** (*Intercambia / Genera / Recibe*): Paso troncal valle central Biobío hacia Araucanía | Estudio Yafún NIC Chile / SUBTEL |
| **`ZCO-IXP`** | **Temuco** (IX) | `-38.732°, -72.592°` | `#230` | 3 | `#1` | **IXP / PIT Regional / Troncal** (*Genera / Intercambia / Recibe*): PIT Temuco, agregación Araucanía y salida Pino Hachado | PIT Chile / SUBTEL / Estudio Yafún |
| **`ZAL-TRN`** | **Valdivia** (XIV) | `-39.814°, -73.246°` | `#1851` | 3 | `#1` | **Nodo Troncal Regional** (*Genera / Intercambia / Recibe*): Cabecera Los Ríos y nodo científico REUNA/UACh | REUNA / SUBTEL / Estudio Yafún |
| **`ZOS-TRN`** | **Osorno** (X) | `-40.573°, -73.132°` | `#659` | 3 | `#3` | **Nodo Troncal / Paso Internacional** (*Intercambia / Genera / Recibe*): Cruce internacional Cardenal Samoré hacia Argentina | SUBTEL / Estudio Yafún |
| **`PMC-CLS`** | **Puerto Montt** (X) | `-41.469°, -72.938°` | `#661` | 3 | `#3` | **Aterrizaje Submarino / IXP Sur** (*Genera / Intercambia / Recibe*): PIT Puerto Montt y cabecera norte cables submarinos Gtd/FOA | SUBTEL (FOA) / PIT Chile / Yafún |
| **`CCH-CLS`** | **Castro / Quellón (Chiloé)** (X) | `-42.481°, -73.762°` | `#667` | 3 | `#3` | **Aterrizaje Submarino / Insular** (*Intercambia / Recibe / Genera*): Troncal Chiloé y aterrizaje submarino Quellón hacia Aysén | SUBTEL / Estudio Yafún |
| **`GXQ-TRN`** | **Coyhaique / Pto. Chacabuco** (XI) | `-45.571°, -72.068°` | `#64` | 3 | `#3` | **Aterrizaje Submarino / Troncal Austral** (*Genera / Intercambia / Recibe*): Cabecera Aysén vinculada a CLS Puerto Chacabuco | SUBTEL (FOA) / Estudio Yafún |
| **`PUQ-CLS`** | **Punta Arenas** (XII) | `-53.159°, -70.913°` | `#1907` | 3 | `#4` | **Aterrizaje Submarino (FOA) / DC Austral** (*Genera / Intercambia / Recibe*): Cable Fibra Óptica Austral y hub Magallanes/Antártica | SUBTEL (FOA) / Estudio Yafún |

---

## 3. Criterio Topológico Complementario (`cnt >= 3` en `red_troncal_vertices_pgr`)
Además de los **23 Nodos Clave Estratégicos** con nombre e infraestructura crítica identificada, la tabla `red_troncal_vertices_pgr` contiene **367 vértices de conmutación e intercambio con grado $\ge 3$** ($315$ de grado 3, $50$ de grado 4 y $2$ de grado 5), descartando los $3.650$ vértices de grado 2 (`80,11%`) que solo representan puntos intermedios de continuidad lineal en los shapefiles. Ambos conjuntos (los **23 Nodos Estratégicos** y los **367 Nodos Clave Topológicos**) se evalúan simultáneamente en todos los scripts y en el visor Leaflet.
