# THERMALIA — Base maestra de manifestaciones termales de Chile (Fase 2b–2d, recopilación ampliada)

Fecha: 21 de octubre de 2026. Esta base se construyó solo con la carpeta del proyecto y fuentes públicas (literatura, catastros, directorios turísticos, tesis, prensa, videos y redes). Los ~100 sitios del Núcleo Milenio se incorporarán al final del proyecto. Está pensada para publicarse en GitHub Pages (`fissotta/thermalia`): el GeoJSON alimenta el mapa y el JSON las fichas.

## 1. Archivos

| Archivo | Contenido |
|---|---|
| `termas_chile_master.json` / `.jsonl` | **303 manifestaciones termales** (balnearios, manantiales naturales, géiseres, fumarolas, pozas hirvientes, vertientes de salar, baños históricos), un registro por manifestación con ~70 campos (valor `NA` cuando no se encontró el dato). Cada registro tiene un campo **`capa`**: `documentada` (167: tiene T, pH, química, estudios o tesis), `catastro/directorio` (79: solo nombre y ubicación en D.S. 142/2000, Hauser o directorios turísticos), `mencionada` (31: nombrada en listados o GVP/Wikipedia sin datos ni coordenadas firmes) e `histórica` (26: baños descritos por Darapsky 1890, Asta-Buruaga 1899, Risopatrón 1924 o la Guía del Veraneante 1944, con estado actual desconocido). Las versiones anteriores se conservan en `termas_chile_master_v1_200.json` y `_v2_241.json`. |
| `termas_chile_master.csv` | Misma base aplanada (listas unidas con ` | `) para revisar en Excel/Sheets. |
| `termas_chile.geojson` | 235 manifestaciones con coordenadas, listo para Leaflet/MapLibre (`properties.capa` permite encender/apagar cada capa). |
| `tesis.jsonl` | 111 tesis y memorias (8 universidades) con link; 73 termas tienen al menos una tesis asociada. |
| `medios.jsonl` | 218 ítems: 112 noticias, 44 videos, 34 redes sociales, 16 documentales/TV, 6 libros/revistas, 6 podcasts. 57 son "generales" (no asignables a una terma). |
| `gazetteer.jsonl` + `gazetteer_README.md` + `raw_gazetteer/` | Lista de 177 lugares con coordenadas y su procedencia (D.S. 142/2000, Hauser 1989, Martini 2008, termasenchile.cl, chiletermas.cl), más tablas crudas y método de conversión UTM. |
| `fichas_norte_centro.jsonl` (51) y `fichas_sur_austral.jsonl` (100) | Fichas detalladas por terma antes de la fusión. |
| `manifestaciones_norte.jsonl` (26) y `manifestaciones_centro_sur.jsonl` (15) | Manifestaciones naturales añadidas en la pasada 2c (fumarolas, campos termales, pozas) desde inventarios científicos y GVP/Wikipedia. |
| `actualizaciones_norte.jsonl` (14) y `actualizaciones_centro_sur.jsonl` (38) | Datos nuevos para registros existentes (Wrage 2017, Alam 2010, Lahsen 1986, Nitschke 2017, Inostroza 2025…); se aplicaron donde había `NA` y, si ya existía valor, quedaron en el campo `actualizaciones` del registro. |
| `manifestaciones_extra.jsonl` (36) y `historico.jsonl` (26) | Pasada 2d: D.S. 142/2000 leído íntegro, Hauser 1997 vía reseñas (Georgudis 1998, Hauser 1999), volcanes con fumarolas (GVP), prensa; y capa histórica (Darapsky 1890, Asta-Buruaga 1899, Risopatrón 1924, Guía 1944). `actualizaciones_extra.jsonl` (30) y `actualizaciones_historico.jsonl` (44) aportan T, pH, coordenadas e indicaciones históricas a registros existentes. |
| `presencia_digital.jsonl` (98) | Instagram, Facebook, TikTok, YouTube, TripAdvisor (opiniones y rating), Google Maps (solo cuando el operador lo enlaza), contacto y estado operativo según redes, por terma con uso turístico. |
| `ESQUEMA.md` | Diccionario de campos. |
| `merge_master.py`, `merge2.py`, `merge3.py`, `build_gazetteer.py` | Scripts reproducibles de fusión (pasada 2b y 2c) y de conversión de coordenadas. |
| `stats.json` | Cobertura por campo, posibles duplicados y medios generales. |

## 2. Qué hay por región, tipo y capa

Arica y Parinacota 13 · Tarapacá 28 · Antofagasta 33 · Atacama 12 · Coquimbo 6 · Valparaíso 10 · Metropolitana 16 · O'Higgins 7 · Maule 23 · Ñuble 8 · Biobío 16 · La Araucanía 37 · Los Ríos 22 · límite Los Ríos/Los Lagos (Cordón Caulle) 5 · Los Lagos 38 · Aysén 20 · límites Aysén/Magallanes 2 · Magallanes 3 · región por determinar 4.

Por tipo (`tipo_categoria`): manantial/pozón 222 · fumarola 46 · vertiente de salar 8 · géiser 5 (Tatio, Puchuldiza, Alpehue, Lupica, Las Sopas) · pozo 5 · poza hirviente 2 · NA 15.

Por capa: documentada 167 · catastro/directorio 79 · mencionada 31 · histórica 26.

**¿Es un censo?** Se acerca: la literatura habla de más de 300 manifestaciones (Lahsen 2005; Sánchez 2011) y la base ya tiene 303, pero con calidad desigual (ver capas). Lo que sigue faltando son los manantiales individuales de cuatro inventarios bloqueados a lectura automática: Benavente 2016 (~40 de Chile central), Ruiz 2015 (36 de Los Lagos), Negri 2017 (16 de Aysén), Risacher 1999 (vertientes de salares) y la capa Sernageomin del sur; muchos de ellos ya están como registro de catastro y solo les faltan los datos.

## 3. Cobertura por campo (de 303 manifestaciones)

| Campo | Con dato | Comentario |
|---|---|---|
| Coordenadas | 235 | 5 "exactas" (Puyehue, Puyuhuapi, Malleco, Puritama, Tatio, Chancho Ko); el resto "aprox" (pines de directorios, UTM de catastros convertidas) y 3 "dudosas". 23 sin coordenada. |
| Tipo de manifestación | 292 | |
| Origen geológico | 196 | volcánico / falla Liquiñe-Ofqui / falla Pocuro / sedimentario |
| Temperatura medida (M) | 93 (+39 temperaturas históricas de 1871–1944) | Wrage 2017, Alam 2010, Muñoz 2011, Hauser 1989, Inostroza 2025, Tassi 2010, Celis 2012, Faúndes 2022, Gaviria 2016, Muñoz-Saez 2018/2020 |
| Temperatura declarada (D) | 68 | operadores, directorios, Sernatur |
| pH | 46 | |
| Tipo químico | 111 | |
| Iones (resumen) | 82 | |
| Isótopos | 41 | |
| Conductividad | 6 | |
| Arsénico | 12 | |
| Caudal | **0** | ningún dato por terma (solo Tatio y Palguín/Liquiñe en la literatura, a nivel de sistema) |
| Infraestructura | 180 | |
| Categoría (lujo/medio/rústico/natural) | 172 | |
| Operador | 47 | Web 39 · Redes sociales 56 (Instagram 45, Facebook 46, TikTok 6, YouTube 7) · TripAdvisor 45 · Google Maps URL 10 · Contacto/reservas 44 · Precio declarado 32 |
| Barros | 22 | caracterizado (Puyehue, Cañón del Blanco) / declarado / informal |
| Propiedades declaradas | 34 | Indicaciones históricas 75 |
| Pueblo originario | 96 | Región cultural 44 · Toponimia con fuente 11 · Uso ancestral documentado 8 |
| Área protegida | 28 | Seguridad (ebullición, acidez, accidentes) 26 |
| Estudios enlazados | 168 | Tesis 73 · Noticias 33 · Videos 11 · Documentales/libros 6 |
| En D.S. 142/2000 (fuente geotérmica probable) | 110 | |

Índice `completitud` (0–1, 18 campos clave): la capa `documentada` concentra casi todos los registros ≥0,5; las capas `mencionada` e `histórica` están por construcción cerca de 0.

## 4. Advertencias de calidad (leer antes de publicar)

1. **Coordenadas.** Los pines de termasenchile.cl son a veces genéricos o erróneos (Porcelana desviada 56 km, Puerto Bonito 230 km, Juncalito 76 km; Molulco y Trancura comparten pin; el complejo de Liquiñe tiene 6 centros a <1 km con pines aproximados). Regla aplicada: fuente científica u oficial manda; el pin del directorio queda en `fuentes_coord_alt`. Las UTM del D.S. 142/2000 y de Hauser 1989 no declaran datum (probablemente PSAD56: desplazamiento de 200–400 m no corregido). 18 registros llevan nota `DISCREPANCIA`. Dos coordenadas erróneas de la fusión automática se retiraron (Río Blanco de Curacautín; Aguas Calientes de General Lagos).
2. **Sernageomin MapServer "Geoquímica de Emisiones Termales"** (coordenadas, T, pH, CE e iones de Araucanía a Los Lagos) **no pudo descargarse desde este entorno** (proxy/robots). Es la pieza más valiosa pendiente: descargarlo desde un navegador normal (`.../MapServer/0/query?where=1%3D1&outFields=*&f=json`) y cruzar por cercanía <2 km. Lo mismo para Wikidata, Overpass/OSM y GeoNames (consultas listas en `gazetteer_README.md`).
3. **Tablas de tesis de la U. de Chile** (Benavente 2015, Berríos 2015, Celis 2012, Allende 2017, Negri 2017, Pincetti 2016, Ruiz 2015, Sánchez-Alfaro 2010) están bloqueadas a lectura automática: se citan con sus rangos pero sin los valores por manantial. Abrirlas en navegador y transcribir sus tablas sumaría T/pH/iones a ~60 termas más.
4. **Google Maps y seguidores de redes**: Google no permite lectura automática (ratings, n.º de reseñas y coordenadas canónicas quedan `NA` salvo 10 enlaces publicados por operadores); Instagram/Facebook/TikTok tampoco entregan seguidores. Ambas cosas se pueden completar en lote con el navegador integrado cuando el computador esté conectado (funcionó para Chancho Ko). Las coordenadas de fumarolas corresponden a la cumbre del volcán (GVP/Wikipedia), no al campo fumarólico.
8. Alias cruzados retirados en 2d (Chinchillani en Chillán, Risopatrón en Catillo, Los Barros/Barroso en Mamiña, Sopas/Venados en Baños de Azufre, Salar Aguas Calientes en Aguas Calientes de General Lagos, Rinconada en El Rincón); Molulco marcado como posible duplicado de Balboa; tres coordenadas incompletas de la capa histórica retiradas. Los registros `histórica` traen cita textual y obra/página; su `estado` indica si existen con otro nombre, desaparecieron o es desconocido.
7. Correcciones aplicadas en 2c: redes sociales cruzadas entre termas homónimas (Aguas Calientes de Puyehue vs. General Lagos/Chillán; Valle de Colina vs. Termas de Colina; Puyuhuapi Lodge vs. Ventisquero) eliminadas; alias de Río Liquiñe y Coñaripe separados; El Tatio: cuenta oficial `geisers.deltatio`. Estado operativo: Los Pozones cerrado desde 09-03-2026; Geométricas deja el predio el 30-09-2026; El Amarillo "permanently closed" en TripAdvisor.
5. **Tres tesis** (`verificado: false`) tienen autor/año sin confirmar.
6. Los valores en texto (p. ej. `"Roca Verde 68 (M); Casa Roja 82 (M)"`) mezclan varios manantiales del mismo complejo: al modelar la base (Fase 3) conviene separar `terma → manantial → muestra`.

## 5. Lo más útil que apareció en la recopilación ampliada

- **Tesis con datos medidos** (todas con link en `tesis.jsonl`): Pincetti 2016 (Plomo, Morales, Colina: As >200× la norma en Baños Morales), Sánchez-Alfaro 2010 (11 áreas Villarrica–Chihuío), Celis 2012 (Puyehue), Muñoz 2011 (Sierra Nevada, Manzanar, Malalcahuello), Benavente 2015 (Chile central), Ruiz 2015 (18 de 36 termas de Los Lagos), Martini 2008, Negri 2017 y Allende 2017 (Aysén), Berríos 2015 (Chillán, Copahue), Lagos 2016 y Tort 2017 (Surire), Wechsler 2024 (Láscar), Faúndes 2022 (Catillo: 17 muestras y medicina termal), Dorsch 2003 (Puyehue). También 15 tesis de arquitectura de centros termales y 10 de turismo.
- **Prensa reciente relevante**: Termas Geométricas deja Coñaripe el 30-09-2026 (el recinto sigue como "Termas Martini"); incendio total del Hotel Alto Nevados de Chillán el 06-09-2026 (reapertura 2027); caso Legionella en Panimávida 2022–23 con cierre sanitario; conflicto Puritama–comunidad de Solor 2015 y Reserva de Conservación Puritama (2024); Chusmiza: fallo 2009 y acuerdo 2022; Kokiyen reabre 2019; Nitrao cedida a Trapa Trapa 2020; Transtour (grupo Schiess) toma control de Puyehue 2016.
- **Divulgación**: libro *Descubriendo las termas del Altiplano chileno* (Eyzaguirre, Ladera Sur, 40 termas con ficha técnica, no digitalizado); tres "Rutas termales" de Revista Enfoque (2022); canal CEGA Geotermia; capítulos de *Lugares que hablan* (Alto Biobío, Hornopirén, Chillán) y *Siguiendo Huellas: Géiseres del Tatio* (BioBioTV 2026); TikTok @martinhowardg "La Ruta de las Termas". No se hallaron capítulos específicos de *Chile Conectado*, *Frutos del País* ni documentales NatGeo/Discovery sobre el Tatio.

## 6. Próximos pasos de datos (antes o durante la Fase 3)

1. Descargar el MapServer de Sernageomin y las consultas Wikidata/OSM desde un navegador y correr `merge_master.py` de nuevo.
2. Transcribir las tablas de las tesis bloqueadas (lista en §4.3).
3. Pedir a Sernageomin el catastro Hauser 1997 (Boletín 50) y a Ladera Sur las fichas del libro de Eyzaguirre.
4. Verificar coordenadas de las 23 termas sin pin y de las marcadas `DISCREPANCIA`/`dudosa` (Google Maps en navegador).
5. Separar en el modelo final terma → manantial → muestra, y mantener siempre la etiqueta M/D.
