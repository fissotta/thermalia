# THERMALIA — Fase 1: Inventario de la carpeta `Plataforma_THERMALIA`

Fecha: 21 de octubre de 2026. Método: lectura de los 110 archivos de la carpeta (PDF, DOCX, PPTX, TXT) más OCR de las 160 capturas de pantalla. Los PDF escaneados sin capa de texto se leyeron por OCR de muestra (se indica cuando aplica). Nada de lo que sigue proviene de internet: es solo lo que hay en la carpeta.

---

## 1. Visión general

La carpeta contiene **110 documentos** (104 PDF, 2 DOCX, 1 PPTX, 1 TXT sin extensión, 1 carpeta con 160 PNG) más el PDF `Compilado_Termas.pdf`, que es exactamente la compilación de esas 160 capturas. Descontando duplicados exactos (hay 9), quedan **~100 documentos distintos**.

El acervo está fuertemente sesgado hacia **(a) medicina termal y peloides (barros)**, con mucha literatura española, italiana y argentina, y **(b) fuentes históricas chilenas del siglo XIX y de 1935–1972**. La geoquímica *medida* de termas chilenas está en solo **4 documentos** (Hauser 1989, Martini 2008, Wechsler 2024 y un resumen de congreso sobre Cañón del Blanco), y no hay ningún dataset tabular (CSV/XLSX) ni archivo geoespacial. No hay microbiología de termas chilenas; toda la microbiología/biología termal con datos corresponde a Copahue–Domuyo (lado argentino).

### Categorías de información presentes

| Cat. | Categoría | N.º docs | Qué aportan para el mapa |
|---|---|---|---|
| A | Fuentes históricas chilenas (1871–1972) | 18 | Historia, usos medicinales declarados, temperaturas y "clasificación" de la época, publicidad de hoteles termales, altitud y distancias |
| B | Catastros y geoquímica de termas chilenas | 6 (+6 contexto) | T, pH, conductividad, iones mayores, Piper, isótopos, geotermometría, origen estructural (fallas), coordenadas UTM de 42 fuentes |
| C | Peloides / barros termales | 27 | Composición, propiedades térmicas, mineralogía, microbiología, seguridad (metales), usos; **datos chilenos solo de Puyehue y Cañón del Blanco** |
| D | Balneoterapia y medicina termal (evidencia clínica, mecanismos, historia) | 21 | Contenido de referencia para el "vademécum": indicaciones, contraindicaciones, clasificación de aguas mineromedicinales |
| E | Microbiología termal y bioactivos (no chilenos) | 8 | Marco conceptual para la capa biológica; bioseguridad |
| F | Turismo, cultura y etnias (web, prensa, Wikipedia) | 12 | Listados de termas por región, servicios, precios, relatos ancestrales (pewenche, aymara, mapuche) |
| G | Capturas de pantalla (160) / Compilado | 1 | Listados regionales de termasenchile.cl, Google Maps de 13 termas, mapas My Maps, visores Sernageomin/DGA, guías "Turismo sobre ruedas" |
| H | Documentos del proyecto MN-Thermalia | 2 | Texto de outreach y figura del marco de muestreo (~100 termas) |
| — | No pertinentes / ruido | 5 | Informe Inodú 2018 (carbón), organigrama Sernageomin, CV, página hackeada, texto generado por IA sobre patógenos |

---

## 2. Inventario detallado por categoría

### A. Fuentes históricas chilenas (siglo XIX – 1972)

| Archivo | Tipo | Año | Termas cubiertas | Variables / contenido | Estado |
|---|---|---|---|---|---|
| `Domeyko_1871_Aguas minerales de Chile.pdf` (69 pp) | Monografía científica (Imprenta Nacional) | 1871 | Apoquindo, Colina, Cauquenes, Chillán, Panimávida, Catillo, San Fernando (Flaco), Baños del Toro, Socos, Jahuel, Petrohué, Sotomó, Cahuelmó, Llancahué, Nitrao, manantiales del Fierro, Litre, Mejillones, Inca | Análisis químicos de la época (sales, gases), temperatura, clasificación por composición, observaciones geológicas | Texto OCR aceptable; es **la base histórica** del vademécum |
| `Aguas termales de Chillan.pdf` (137 pp, 360 MB) | Libro: P. Martín, *Baños de la Cordillera. Estudios médicos sobre las aguas termales de Chillán*, 3.ª ed. (Valparaíso) | c. 1866–1870 (cita análisis 1851–1866) | Chillán (y comparaciones con Apoquindo, Aguas Calientes, Nitrao, Pica, Porcelana) | Historia, caracteres físico-químicos, temperaturas por fuente (p. ej. "42 °C"), propiedades terapéuticas, indicaciones y contraindicaciones | OCR regular |
| `El manual de bañista.pdf` (40 pp, MC0072596) | Guía de baños minerales de Chile (Dr. J. Miquel) + Cauquenes (Dr. F. Tocornal) | s. XIX | Cauquenes, Colina, Apoquindo, Chillán, Corazón | Reglas higiénicas, modo de tomar baños, propiedades | OCR aceptable |
| `MC0072597.pdf` (19 pp) | *Manuales de higiene física y moral II: Higiene en el verano* | s. XIX–XX | Balnearios de **España** | Balneografía e hidroterapia; no chileno | Contexto |
| `Aguas termales de Panimavida.pdf` (24 pp, MC0072932) | Cartilla médica (Dr. F. Hederra) | s. XX temprano | Panimávida, Corazón | Factores de la cura termal, indicaciones | OCR aceptable |
| `183467.pdf` (28 pp) | Memoria científica, Instituto de Hidrología y Climatología Médicas de Panimávida (Dr. F. Bravo) | 1939 | Panimávida | Clínica termal, casuística | Texto OK |
| `Notas de prensa Termas_1944.pdf` (67 pp, 92 MB) | *Guía del Veraneante 1944* (FF.CC. del Estado), sección zona central/sur | 1944 | Cauquenes, San Fernando, Panimávida, Cachantún, Chillán, Catillo, Tolhuaca, Río Blanco, Manzanar, Porcelana, Tanhuao | Temperaturas declaradas ("40–50°"), sales, indicaciones, acceso, altura | OCR regular |
| `Informacion aguas termales de chile_1944.pdf` (6 pp) y `Informacion aguas termales de chile.pdf` (4 pp) | Misma guía 1944, capítulo "Informaciones sobre las más importantes aguas termales de Chile" | 1944 | Jahuel, Apoquindo, Auco, Catillo, Palguín, Río Blanco, Chillán | Altura, presión, clima, clasificación ("homotermales, hipotónicas, radioactivas, oligometálicas") | OCR regular; **posible duplicado parcial** |
| `Nota sobre las aguas termales de chile.pdf` (3 pp, MC0014438) | Revista *En Viaje* (FF.CC.) | 1940 | Jahuel, Colina, Corazón, Tolhuaca, Río Blanco, Palguín, Puyehue | Reportaje, "curaciones", barro mineralizado | OCR pobre |
| `Termas del flaco.pdf` (3 pp) | Artículo de revista (ilustrado) | c. 1940s | Termas del Flaco / Las Vegas (San Fernando), Baños del Toro | Origen del nombre, altitud (1.730 m), relato | OCR pobre |
| `MC0074622.pdf` | Aviso publicitario | c. 1935–44 | Cauquenes | "Mejor establecimiento termal", clima | 1 pág. |
| `MC0074623.pdf` | Aviso (escaneado) | c. 1935–44 | Tolhuaca | "Aguas más importantes según análisis del cordón andino"; reumatismo, vías respiratorias | OCR hecho |
| `MC0074624.pdf` | Aviso | 1935–36 | Río Blanco (Curacautín) | Temporada, capacidad hotel (120), altura 1.050 m, precios | OK |
| `MC0074634.pdf` | Aviso (escaneado) | c. 1935–44 | Chillán | "Saturado de radioactividad" | OCR hecho |
| `MC0074665.pdf` | Aviso (escaneado) | c. 1935–44 | Catillo | "Únicas aguas litinadas del país" | OCR hecho |
| `MC0074721.pdf` | Aviso (escaneado) | c. 1935–44 | Panimávida | Publicidad | OCR hecho |
| `MC0074750.pdf` | Aviso | c. 1935–44 | Menetúe ("Minetue") | "Aguas radioactivas", reumáticas y cutáneas | OK |
| `MC0074769.pdf` | Aviso Sociedad de Turismo y Hoteles de Chile | c. 1935–44 | (hotel termal con "baños de barro curativo", planta embotelladora; probablemente Puyehue) | Servicios | OK |
| `MC0074771.pdf` | Aviso (escaneado) | c. 1935–44 | Puyehue | "Gran hotel termal, 150 departamentos, baño termal privado" | OCR hecho |
| `MC0072916.pdf` | Aviso | ? | ilegible | — | OCR ilegible |
| `Asociación Termal de Chile_1972_aguas termales de chile.pdf` (3 pp) | Ponencia Seminario Uso de Recursos de Agua | 1972 | Mamiña, Socos, Colina, Cauquenes, San Fernando, Panimávida, Quinamávida, Catillo, Chillán, Manzanar, Río Blanco, Palguín, Puyehue (+ más en la tabla) | **Tabla: altitud, temperatura del agua, distancia a ciudad** para los principales establecimientos; menciona Primer Congreso de Aguas Termales (Panimávida 1971) y necesidad de legislar "fuente curativa" / "barros minero-medicinales" | Texto OK |
| `Las termas como atractivo turístico - Memoria Chilena.pdf` | Página web BN | s/f (2026 captura) | Chillán, Cauquenes, Catillo, Tolhuaca, Puyehue, Flaco, Menetúe, Palguín | Historia del turismo termal 1870–1975 | OK |

### B. Catastros y geoquímica de termas chilenas

| Archivo | Tipo | Año | Termas / zona | Variables medidas | Estado |
|---|---|---|---|---|---|
| `Hauser_1989_FUENTES TERMALES Y MINERALES EN TORNO A LA CARRETERA AUSTRAL…pdf` (10 pp) | Paper, *Revista Geológica de Chile* 16(2):229-239 | 1989 | **25 fuentes** Regiones X–XI: Pichicolo, Río Blanco, Llancahué, Cahuelmó, Porcelana, Chilco, El Peñón, Lago Negro, El Amarillo, Michinmahuida, Yelcho, Moraga, Santa Lucía, Puerto Bonito, Puyuhuapi, Aeropuerto, Queulat, Trapananda, Chilconal, Huemules, Cupquelán, Huiña, El Engaño, Quitralco, Cristal | Coordenadas UTM (Tabla 1), **temperatura (23–84 °C), pH, iones mayores, hierro, Piper (Tabla 2)**, caudal cualitativo, relación con ZF Liquiñe-Ofqui, cuáles tienen balneario (5) | Texto OK; **la Tabla 2 (química) no se extrajo bien y debe transcribirse a mano desde el PDF** |
| `martini_2008_catastro de termas de chile.pdf` (154 pp) | Memoria de título Geología, U. de Chile (S. Martini) | 2008 | **22 fuentes** Cordillera Principal 32°30'–34°S; 17 con geoquímica: Jahuel, La Higuera (2), El Barro, Corazón (2), Auco, Saladillo, Chacabuco, Colina Peldehue, Carvajalino, Tupungato, Salinillas, El Plomo, Baños Morales, Colina Maipo, Puente de Tierra | UTM + altitud (Tabla 2), iones mayores, familias (carbonatadas ZF Pocuro–San Ramón vs cloruradas ZF El Diablo–El Fierro), geotermómetros de sílice y cationes (70–180 °C de reservorio), isótopos δ18O/δ2H, flujo calórico, contexto estructural; capítulo de usos de la geotermia y potencial de Chile | Texto OK; **mejor fuente de datos para la zona central** |
| `wechsler_2024_GEOQUÍMICA DE LAS AGUAS TERMALES … VOLCÁN LÁSCAR.pdf` (13 pp) | Tesis/artículo, U. de Concepción | 2024 | **15 vertientes** en 4 valles (Hécar, Catarape, Talabre, Sóncor), Antofagasta | Química e isótopos, aguas cloruradas maduras, geotermometría (>200 °C profundo; 50–80 °C somero), lineamientos por sensores remotos; cita Hauser (1997) para Ojos de Hécar | Texto OK |
| `Caracterización del peloide de las Termas Cañon del Blanco de Chile.pdf` (185 pp) | Libro de resúmenes IX CIBAP 2025 (Arnedillo, España); el resumen chileno está en p. 115 | 2025 | Cañón del Blanco (Araucanía, volcán Sierra Nevada) | **Agua: pH 7,94; CE 180 µS/cm; residuo seco 116 mg/L; Cl 13,8; HCO3 47,2; SO4 17,1; Na 12,3; Mg 3,2; Ca 10,5; K 2,8; Si 15,5 mg/L. Peloide: pH 2,72, 35 % agua, densidad 1.370 kg/m³, Cp 2.030 J/kg·K, k 1 W/m·K, sulfatos 13 g/kg, cuarzo 16 %, arcillas 8 %, pirita 6,5 %**; línea cosmética Trawe | Dato medido en laboratorio (U. da Coruña) |
| `03-PeloidesdePuyehue_Lorena_Vela.docx` | Resumen de congreso (Vela, Armijo, De Gracia, Schiess, Maraver; UCM + Termas de Puyehue) | s/f (c. 2023–25) | **Termas de Puyehue**, 3 pozos | Composición centesimal (sólidos 25,6/32,5/46,2 %; agua 74,4/67,5/53,8 %; cenizas), capacidad calorífica (3.407/3.178/2.710 J/kg·K), conductividad térmica (~0,45 W/m·K), retentividad, tiempos de relajación (7,8/9,0/9,6 min); toponimia mapudungún (*puye* + *we*) | **Dato medido**; no incluye química del agua |
| `Mapa de fuentes de aguas termales de Chile.pdf` (2 pp) | Ficha de repositorio DGA del mapa de Hauser (Sernageomin) | 2000 | Todo Chile | Solo metadatos (escala 1:3.000.000, resumen). **El mapa en sí no está en la carpeta** | Falta el mapa |
| `Geotermia-en-Chile-un-siglo-de-historia…pdf` (240 pp, CEGA) | Libro | 2022 | Nacional (Tatio, Puyuhuapi, Liquiñe, Cauquenes, Chillán, Tolhuaca, Cerro Pabellón, Aysén, Lirima, Surire, Juncalito, Puchuldiza, etc.) | Historia de la exploración geotérmica, potencial, usos directos, comunicación social; sin tablas por terma | Texto OK; contexto geológico y social |
| `Ranking-2023_tabloide_20231012.pdf` | Ranking de riesgo de volcanes Sernageomin | 2023 | Sistemas volcánicos (Villarrica, Calbuco, Llaima, Puyehue–Cordón Caulle, Láscar, Copahue…) | Posición de riesgo | Útil para capa "origen volcánico" |
| `Patrimonio Geológico … Nevados de Chillán-Laguna del Laja (Ladera Sur).pdf` | Artículo divulgación | 2017 | Chillán | Geopatrimonio, reserva de biósfera | OK |
| `Estudio … potencial geotérmico de hasta 3.800 MW (Min. Energía).pdf` | Noticia | 2018 | Nacional | Potencial 1.300–3.800 MW | Contexto |
| `informe-final-mesa-geotermia.pdf` (70 pp) | Informe Mesa de Geotermia | 2018 | Nacional | Rol de la geotermia eléctrica | Contexto |
| `THERMALIA_Annex1_Map_Methods.pptx` | Figura del proyecto | 2026 | ~100 termas (marco de muestreo MN-Thermalia) | Solo imagen del mapa y flujograma; **no contiene la lista ni coordenadas** | Falta la tabla fuente |

### C. Peloides / barros termales (27 archivos, 19 distintos)

**Con datos de barros sudamericanos:**

| Archivo | Año | Sitio | Contenido |
|---|---|---|---|
| Vela et al., Puyehue (docx) | c. 2024 | Puyehue (Chile) | ver tabla B |
| CIBAP 2025, Cañón del Blanco | 2025 | Cañón del Blanco (Chile) | ver tabla B |
| `Basualdo_2011_Actividad antimicrobiana de fangos de Copahue.pdf` | 2011 | Copahue, **Laguna Sulfurosa** (Arg.) | Actividad inhibitoria de la fase líquida frente a *S. aureus*, *C. albicans*, *E. faecalis* |
| `Cianobacterias de copahue.pdf` = `Flores de melo.pdf` (duplicado) | 2019 | Copahue (Arg.): lagunas Verde, Sulfurosa/Madre, del Chancho, Baño 9, Las Máquinas | Cianobacterias ácido-termófilas, taxonomía; T y pH de cada laguna |
| `FloresMelo_2021_Caracterizacion limnologica.pdf` | 2021 | Copahue (Arg.) | Caracterización fisicoquímica de agua, algas y fangos usados terapéuticamente (**la mejor fuente sobre la Laguna Madre/Sulfurosa**) |
| `Ubogui_2008_Seguimiento clínico de pacientes con psoriasis.pdf` | 2008 | Copahue (Arg.) | PASI antes/después en psoriasis |
| `Buscan resguardar los fangos termales de Copahue_.pdf`; `pdf7929.pdf` | 2007 / s/f | Copahue (Arg.) | Prensa: fango natural como recurso no renovable, fango madurado artificial (EPROTEN–U. Comahue) |
| `Accorinti_1991`, `Accorinti_1995` (×2) (escaneados sin OCR), `Accorinti_2005`, `Accorinti_2006` | 1991–2006 | Domuyo y Copahue (Arg.) | Algas termales: actividad antibacteriana/antifúngica, promotores de crecimiento celular, nucleósidos, fitohormonas |

**Revisiones y métodos (no chilenos):** Carretero 2020 Parte I y Parte II (`j.clay.2020.105531.pdf` es duplicado de la Parte II); Gomes 2015 (peloides naturales vs diseñados); Maraver et al. 2021 *Peloids as Thermotherapeutic Agents* (×2 duplicado; incluye Copahue y Puyehue entre comparaciones); Mourelle 2021 *Microalgal peloids* (×2 duplicado); **Mourelle et al. 2025 *Development of a microalgal peloid* aparece 4 veces** (`484_2025_Peloides`, `Development of a microalgal peloid`, `Maria Lourdes Mourelle_Peloide VIgo CHILE`, `Mourelle_2025_Rosmarinic acid`); Ortega-Collazos 2025 (peloide con ácido rosmarínico, artrosis); Park 2024 (peloide submarino Corea, metales pesados); Bastos 2024 (absorción percutánea de elementos tóxicos en peloides sulfurosos); Baldovin 2020 (higiene microbiológica de fangos, Abano); Hoteteu 2018 (Techirghiol); Pipite 2023 (lodos de Fiji, antimicrobianos y metales).

### D. Balneoterapia y medicina termal (21)

Armijo, *Aguas minerales y mineromedicinales: mecanismos básicos de acción* (`8_aguas.pdf`); García Matas 2006 (tipos de aguas, aplicaciones, indicaciones y contraindicaciones; Junta de Andalucía); AETS/ISCIII 2006 *Técnicas y tecnologías en hidrología médica e hidroterapia* (219 pp); **`vademecum.pdf` = *Vademécum de aguas mineromedicinales españolas* (ISCIII, 310 pp, escaneado sin OCR)** — es el modelo de ficha que inspira la capa "vademécum" (por balneario: propiedades físicas, química, radiactividad, técnicas crenoterápicas, indicaciones); Cochrane 2015 (artritis reumatoide); Protano 2024 (dermatología, revisión sistemática); Cheleschi 2021 (mecanismos en reumatología); Maccarone 2021 (respuesta inmune); Mennuni 2021 (metaanálisis fangoterapia en artrosis de rodilla); Bazzichi (fibromialgia); Mao (hidroterapia termal y lumbalgia); Habek (balneoginecología); Morer 2017 (rol de elementos minerales, ensayos doble ciego); Ferrara (Saturnia, interrupción COVID); caso clínico Dialnet 2009; Gianfaldoni 2017 e van Tubergen 2002 (historia de los baños); spadreams (web comercial); Alvareda et al. 2026 (Uruguay, Guaraní: **buen modelo metodológico**: Piper, Gibbs, clasificación balneológica de 7 fuentes); Andueza 2018 (microbiología de aguas mineromedicinales en Latinoamérica, resumen de conferencia); CV de Lorena Vela.

### E. Microbiología termal y bioactivos (8)

Calhoun et al. 2026 (crenarchaeol en 41 fuentes de Yellowstone + compilación global; coautor de U. Santo Tomás, Chile); Wirajana 2026 (revisión: microbios, metabolitos y minerales de hot springs); Ansari 2025 (compuestos bioactivos disueltos, Ladakh, GC-MS); Roy 2023 (actividad antimicrobiana agua de Bakreshwar); Daddy 2024 (metagenómica de aguas subterráneas para productos farmacéuticos); HS076 y HS651 (grupos de riesgo de microorganismos, UNSW); FDA (endotoxinas/pirógenos); `Natural and thermal water sources can host a variety of pathogens.docx` — **texto generado por un asistente de IA, sin fuentes; no debe citarse**.

### F. Turismo, cultura y etnias (12)

gochile.cl *Las 10 mejores termas* (Polloquere, Puritama, Huife, Pozones, Geométricas, Malalcahuello, Coñaripe, Pellaifa, Puyuhuapi, El Plomo…); chileestuyo.cl *Termas 2025* (Puritama, Jurasi, Polloquere, Surire, Chillán, Puyehue, Ventisquero, Quinamávida…); Andes Campers *Ruta de Termas & Spas*; termasenchile.cl (página capturada **hackeada**, inútil); Wikipedia Termas de Cauquenes (coordenadas, altitud 760 m, historia); Wikipedia *Mapuche medicine* (aguas termales en la medicina mapuche; fuente secundaria); **Centro Termal Pehuenche Kokiyen, Alto Biobío (Comité Indígena CORFO, 2019)** — turismo ancestral de la comunidad de Cauñicu (única fuente directa sobre uso indígena actual); Wellness Club Parque Termal Botánico Pucón (publirreportaje 2025); Estrategia Nacional de Turismo Sostenible 2035 (Subsecretaría de Turismo; marco de política, sin datos por terma); Baños de Apoquindo (captura de web vacía); Hidrología médica spadreams.

### G. Capturas de pantalla (160 PNG = `Compilado_Termas.pdf`)

Contenido identificado por OCR: (1) figura de flujo calórico de Martini 2008; (2) guías "Turismo sobre ruedas" / revista *Enfoque* (H. Merino): **Ruta termal del Norte (Visviri–Socos), del Centro (San Felipe–Nitrao, "~50 fuentes") y del Sur (Laguna Laja–Seno Skyring)** con fichas breves de ~40 termas (categoría: de lujo / sencillas / rústicas; servicios; cómo llegar; estado en pandemia); (3) mapas Google My Maps de termas (zonas Todos los Santos–Rupanco, Laguna de los Patos, Cajón del Maipo, Laguna del Azufre/volcán San José); (4) fotos y reseñas de Google Maps de **Cahuelmó, Rañintulelfu (Huilo Huilo), El Rincón, Geométricas, Quimey-Co, Río Blanco (naturales), Cañón del Blanco, Chihuío, Porcelana, Llancahué, Pichicolo, "Chancho Ko", Aguas Calientes de Chillán**; (5) listados por región de termasenchile.cl (Arica a Magallanes; p. ej. Tarapacá: Chusmiza, Ancuaque, Puchuldiza; Maule: Antemávida, El Médano, Campanario; Biobío: Valle Hermoso, Kokiyen/Chichintahue, Nitrao; Los Ríos: Río Hueico, Cofre, Huilo Huilo, Quilalelfu, Carranco, Punulaf, Trafipán, Rayenco, Hipólito Muñoz, Vergara, Manquecura, Pellaifa, Chihuío, Llifén, Río Liquiñe; Aysén: Ensenada Pérez, Chilconal, Ventisquero, Puyuhuapi; Magallanes: sin resultados); (6) visores: Sernatur, **Sernageomin ArcGIS Experience (Sistema Abierto / Sistema Vertical)**, repositorio DGA; (7) perfil LinkedIn de Miria Baschini (U. Comahue, peloides Copahue), cremas Caviahue, video volcán Copahue, Asociación Termal de Chile A.G., fotografías de Francisco Gedda, hotel Refugio.

Nota sobre **"Chanchoco"**: en la carpeta no aparece ese nombre. Lo más cercano son tres capturas de Google Maps de **"Termas De Chancho Ko"** (sin ubicación legible). Necesito que me confirmes si es la misma terma y dónde está.

### H. Proyecto

`THERMALIA_Outreach and Connections with Other Sectors` (sección 5.3 de la propuesta: base de datos Thermalia de ~100 termas, web, exposición itinerante, kit educativo, podcast, operadores Puyehue y Aguas Calientes); `THERMALIA_Annex1_Map_Methods.pptx` (marco de muestreo nacional y flujograma SO1–SO5).

### Duplicados exactos (9) y archivos descartables

Duplicados: Mourelle 2025 ×4; Maraver 2021 ×2; Mourelle 2021 ×2; Carretero Parte II ×2; Flores Melo 2019 ×2; `Compilado_Termas.pdf` = carpeta de capturas; Informacion aguas termales 1944 (dos versiones del mismo capítulo). Descartables para la plataforma: Inodú 2018 (cierre de centrales a carbón), organigrama Sernageomin, CV, página hackeada de termasenchile.cl, docx de patógenos generado por IA, HS076/HS651/FDA (bioseguridad de laboratorio, no de termas).

---

## 3. Tabla: qué terma tiene qué tipo de dato en la carpeta

Leyenda: **M** = dato medido en estudio científico; **H** = dato histórico (s. XIX–1972, medido con métodos de la época); **D** = dato declarado por sitio turístico/prensa; **C** = solo contexto/menciones; **—** = nada.

| Terma (región) | Coordenadas | T / pH / CE | Iones mayores | Isótopos / geotermometría | Microbiología / biología | Barros (peloides) | Propiedades medicinales | Turismo / servicios | Etnia / toponimia | N.º docs |
|---|---|---|---|---|---|---|---|---|---|---|
| **Puyehue** (Los Lagos) ★ | — | H (1972: 50 °C) | — | — | — | **M** (Vela: 3 pozos, físico-térmicas) | H, D | H (avisos 1935–44), D (web, capturas) | M (etimología mapudungún en Vela) | 11 |
| **Aguas Calientes, Puyehue** ★ | — | — | — | — | — | — | — | D (capturas, guías) | — | 3 |
| **El Tatio** (Antofagasta) ★ | — | — | — | — | — | — | — | C (CEGA, Andes Campers, capturas) | — | 4 |
| **Copahue / Laguna Madre** ★ (lado argentino) | — | **M** (lagunas: T, pH) | **M** (Flores Melo 2021) | — | **M** (cianobacterias, algas, antimicrobiano) | **M** (Basualdo, Flores Melo, Maraver) | **M** (psoriasis PASI) + D | D (prensa, cremas Caviahue) | — | 21 |
| **Chanchoco / "Chancho Ko"** ★ | — | — | — | — | — | — | — | D (3 capturas Google Maps) | — | 1 |
| Cañón del Blanco (Araucanía) | — | **M** | **M** | — | — | **M** (completo) | D | D | — | 2 |
| Chillán (Ñuble) | — | H | H (Martín, Domeyko) | — | — | H (barro mencionado) | H | H, D | C | 18 |
| Cauquenes (O'Higgins) | D (Wikipedia) | H (1972: 45 °C) | H (Domeyko) | — | — | — | H | H, D | C | 15 |
| Colina (RM) | **M** (Martini UTM) | **M** | **M** | **M** | — | — | H | D | — | 14 |
| Jahuel, Corazón, Auco, El Barro, La Higuera, Saladillo, Chacabuco, Carvajalino (V/RM) | **M** | **M** | **M** | **M** | — | — | H (Jahuel, Corazón) | D | — | 2–14 |
| Tupungato, Salinillas, El Plomo, Baños Morales, Colina Maipo, Puente de Tierra (RM) | **M** | **M** | **M** | **M** | — | — | — | D (Plomo, Morales) | — | 1–3 |
| Apoquindo (RM) | — | H | H | — | — | — | H | — | — | 7 |
| Termas del Flaco / San Fernando, Baños del Toro | — | H (1972: 60–90 °C) | H (Domeyko) | — | — | — | H | H | — | 5 |
| Panimávida, Quinamávida, Catillo (Maule) | — | H (33/24/36 °C) | H ("litinadas") | — | — | — | H (clínica 1939) | H, D | — | 3–6 |
| Nitrao / Alto Biobío (Kokiyen) | — | — | H (Domeyko menciona) | — | — | — | D | D | **D** (pewenche, Cauñicu) | 5 |
| Tolhuaca, Manzanar, Río Blanco, Malalcahuello, Malleco, Pemehue (Araucanía) | — | H (1972: Manzanar 46 °C; Río Blanco 18–95 °C) | — | — | — | — | H | H, D | — | 1–9 |
| Huife, Menetúe, Palguín, San Luis, Pozones, Quimey-Co (Pucón) | — | — | — | — | — | — | H (Menetúe "radioactiva") | D | — | 1–5 |
| Geométricas, Coñaripe, Liquiñe, Vergara, Trafipán, Pellaifa, Punulaf, Manquecura, Chihuío, Llifén, Hipólito Muñoz (Los Ríos) | — | — | — | — | — | — | — | D | — | 1–5 |
| Ralún, Petrohué, El Callao, Sotomó (Los Lagos) | — | — | H (Domeyko: Petrohué, Sotomó) | — | — | — | — | D | — | 1–5 |
| Pichicolo, Llancahué, Cahuelmó, Porcelana, El Amarillo, Puerto Bonito, Puyuhuapi, Quitralco, Chilconal, Huemules + 15 más (X–XI) | **M** (Hauser UTM) | **M** | **M** (Hauser Tabla 2) | — | — | — | — | D (capturas) | — | 2–7 |
| Hécar, Catarape, Talabre, Sóncor (Láscar, Antofagasta) | ? (ver PDF) | **M** | **M** | **M** | — | — | — | — | — | 1 |
| Jurasi, Polloquere, Chusmiza, Mamiña, Pica, Lirima, Surire, Enquelga, Puritama, Juncalito, Laguna Verde (norte) | — | D | — | — | — | — | D | D | D (aymara: Chusmiza; atacameña: Puritama) | 1–4 |
| Socos (Coquimbo) | — | H (28 °C) | H (Domeyko) | — | — | — | H | D | — | 3 |
| Magallanes | — | — | — | — | — | — | — | D ("sin resultados") | — | 0 |

★ = termas prioritarias del proyecto.

---

## 4. Qué falta o está incompleto para construir las capas del mapa

**Para la capa base (ubicación):**
1. **No hay una tabla nacional de coordenadas.** Solo hay UTM para las 25 fuentes de Hauser 1989 (X–XI) y las 17 de Martini 2008 (zona central) — 42 de las ~100 termas del proyecto. Falta el *Mapa de fuentes de aguas termales de Chile* (Hauser 2000, Sernageomin, 1:3.000.000) del que solo está la ficha de repositorio, y falta cualquier capa del catastro Sernageomin (los visores ArcGIS aparecen solo como capturas).
2. **La lista de las ~100 termas del Nucleus no está** (el pptx trae únicamente la figura).

**Para las capas científicas:**
3. **Geoquímica medida de las termas prioritarias: prácticamente ausente.** Puyehue solo tiene peloides (sin química del agua); Aguas Calientes y El Tatio no tienen ningún dato medido en la carpeta; Copahue tiene datos solo del lado argentino; "Chanchoco" no se identifica.
4. **Iones mayores / tipo de agua** solo para zona central (Martini), Carretera Austral (Hauser; tabla por transcribir), Láscar (Wechsler) y Cañón del Blanco. Nada para Araucanía/Los Ríos (la mayor concentración de termas), Ñuble, Maule, Coquimbo ni norte grande salvo Láscar.
5. **Isótopos y geotermometría**: solo Martini 2008 y Wechsler 2024.
6. **Caudal**: ningún dato cuantitativo (Hauser lo describe cualitativamente).
7. **Microbiología de termas chilenas**: cero documentos; toda la biología es de Copahue–Domuyo (Argentina), Yellowstone, India, Fiji. Es justamente lo que el Nucleus producirá, pero hoy no hay fuente.
8. **Radiactividad**: aparece solo como claim publicitario histórico (Chillán "saturado de radioactividad", Menetúe, Jahuel), nunca medido.
9. **Barros chilenos**: solo Puyehue (físico) y Cañón del Blanco (completo). Chillán (libro de P. Martín), Río Blanco y Manzanar/Curacautín (Guía 1944: "baños a vapor y barro", "barro radioactivo") y, en las guías actuales capturadas, Quinamávida y varios centros de lujo ofrecen "baños de barro", pero sin ninguna caracterización.

**Para las capas turísticas y culturales:**
10. **Infraestructura hotelera**: no hay base estructurada; solo publicidad 1935–44, guías de prensa y capturas con fichas parciales (categoría lujo/sencilla/rústica de la revista *Enfoque*). No hay precios ni temperaturas declaradas sistematizadas por operador; **no están capturados los sitios puyehue.cl ni termasaguascalientes.cl**.
11. **Etnias y toponimia**: solo tres pistas (Puyehue en Vela; Kokiyen/pewenche; Chusmiza/aymara y Puritama/atacameña en capturas) y una página de Wikipedia sobre medicina mapuche. No hay fuentes etnográficas ni de toponimia (p. ej. Augusta, Erize) ni mapeo de pueblos originarios por terma.
12. **Clasificación medicinal por terma**: existe el marco (García Matas, Armijo, vademécum español) pero no una asignación terma-a-indicación con respaldo distinto de la publicidad histórica.

**Problemas de calidad de las fuentes:**
13. Varios escaneos sin texto (Accorinti ×3, vademécum español, avisos) y OCR pobre en revistas de 1940; la Tabla 2 de Hauser debe transcribirse manualmente.
14. Dos capturas de web inservibles (termasenchile.cl hackeada; Baños de Apoquindo vacía) y un documento generado por IA que no debe usarse como fuente.
15. Alrededor del 60 % de la carpeta es literatura de contexto (balneoterapia, peloides, microbiología) de fuera de Chile: muy útil para el vademécum conceptual, pero no aporta datos a ninguna terma del mapa.

---

## 5. Recomendación para cerrar la Fase 1

Lo que la carpeta sí permite ya: (i) una **capa histórica** sólida (Domeyko 1871 → Guía 1944 → Asociación Termal 1972) con temperaturas y clasificaciones de la época para ~20 establecimientos clásicos; (ii) una **capa geoquímica parcial** para zona central, Carretera Austral y Láscar; (iii) dos fichas de **barros** chilenos; (iv) el **marco conceptual completo** para el vademécum (tipos de agua, mecanismos, indicaciones, evidencia clínica) y un modelo de ficha (vademécum ISCIII).

Para la Fase 2 conviene priorizar: catastro Sernageomin/Hauser 2000 (coordenadas), geoquímica de Puyehue, Aguas Calientes, Tatio y Copahue chileno (CEGA, Sernageomin, tesis U. de Chile/Concepción), microbiología de termas chilenas, y fuentes etnográficas/toponímicas.
