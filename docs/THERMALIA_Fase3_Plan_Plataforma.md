# THERMALIA — Fase 3: Plan de la plataforma

Fecha: 22 de octubre de 2026. Plan conceptual previo a cualquier programación. Se apoya en el inventario de la carpeta (Fase 1), la investigación externa (Fase 2) y la base maestra de 303 manifestaciones termales (Fase 2b–2d). El sitio se publicará en GitHub Pages desde `github.com/fissotta/thermalia` (repositorio hoy vacío).

---

## 0. Idea en una frase

Un **vademécum digital e interactivo de las termas de Chile**: un mapa navegable de todo el país donde cada manifestación termal tiene una ficha con dos niveles de profundidad, uno turístico y divulgativo, sencillo y bello, y otro científico con geoquímica, biología, referencias y la ficha de vademécum; sobre el mapa se pueden encender capas que clasifican las termas por origen, temperatura, química, uso, propiedades, cultura, conocimiento disponible e infraestructura. Todo el contenido lleva su fuente y distingue siempre dato **medido (M)** de dato **declarado (D)**.

Principios de diseño que salen de las fases anteriores:
1. La base de datos pública es el prototipo; los ~100 sitios del Núcleo Milenio se suman al final como una capa "Thermalia-MN" sin cambiar la estructura.
2. Honestidad sobre la certeza: cada registro tiene `capa` (documentada / catastro / mencionada / histórica) y cada valor tiene M/D y fuente; donde no hay dato se muestra "sin dato", nunca se rellena.
3. Nada comercial ni de laboratorios: solo contenido de referencia (el vademécum no recomienda tratamientos ni vende análisis).
4. Seguridad explícita: temperatura de ebullición, acidez, arsénico y accidentes se muestran, con el aviso de 1000 Springs: "la temperatura publicada no indica si es seguro bañarse".
5. Sitio estático, abierto y reproducible: datos en CSV/JSON/GeoJSON con licencia abierta, construidos por script, publicados en GitHub Pages; sin backend.

---

## 1. Modelo de datos

### 1.1 Entidades

El modelo separa la **terma** (lugar nombrado y visitable) del **manantial** (manifestación física) y de la **muestra/análisis** (medición en una fecha), porque la base actual mezcla "Termas de Chillán" con "Roca Verde 68 °C; Casa Roja 82 °C; Olla del Mote 91 °C" y el Nucleus entregará muchas muestras por sitio.

```
Terma (sitio) 1 ──< Manifestación (manantial, géiser, fumarola, poza, pozo)
Manifestación 1 ──< Muestra (fecha, campaña, quién) 1 ──< Análisis (parámetro, valor, unidad, método, M/D)
Terma >──< Estudio (paper, tesis, informe)            vía Terma_Estudio (tipo de dato que aporta)
Terma >──< Fuente (web, prensa, video, red social, libro, documento histórico)
Terma >── RegiónCultural 1; Terma >──< PuebloOriginario; Terma 1 ──< Toponimia; Terma 1 ──< UsoAncestral
Terma 1 ──< ServicioTurístico (operador, infraestructura, categoría, precios, horarios, redes, estado)
Terma 1 ──< Barro (peloide): origen, caracterización M/D, usos
Terma 1 ──< PropiedadAtribuida (indicación, quién la atribuye, respaldo)
Terma 1 ──< Taxon/ComunidadMicrobiana (cuando exista: filo dominante, Shannon, metagenoma, BioProject)
Terma 1 ──< Evento (noticia: cierre, incendio, concesión, accidente, erupción)
Terma ── Volcán / SistemaGeotermal / ÁreaProtegida / Comuna
```

### 1.2 Atributos principales (resumen; el diccionario completo está en `ESQUEMA.md` y se ampliará)

- **Terma:** id (slug), nombre, alias, región, comuna, lat/lon + precisión + fuente, altitud, tipo de manifestación dominante, origen geológico, sistema geotermal, volcán asociado, área protegida, `capa` de certeza, `completitud`, estado operativo, administración comunitaria, D.S. 142/2000, texto turístico (2–3 párrafos), texto científico (síntesis), fotos (con licencia y autor), seguridad.
- **Manifestación:** id, terma, nombre local, tipo (manantial, pozón, géiser, fumarola, poza hirviente, poza de lodo, vertiente de salar, pozo), lat/lon propia si existe, T, pH, caudal, descripción.
- **Muestra/Análisis:** fecha, campaña/estudio, parámetros (T, pH, CE, TDS, Na, K, Ca, Mg, Cl, SO₄, HCO₃, SiO₂, B, Li, As, F, Br, Fe, NH₄, gases, δ¹⁸O, δD, ³H, ⁸⁷Sr/⁸⁶Sr, R/Ra, Rn), unidad, método, M/D, fuente. Clasificación hidroquímica derivada (ternario Cl–SO₄–HCO₃; Na-Cl / ácido-SO₄ / HCO₃ / mixta) y geotermometría si la fuente la da.
- **Estudio:** cita completa, año, tipo (fisicoquímico/geoquímico, geológico, biológico, peloides/médico, turístico/social, histórico), DOI/link, acceso abierto o no, termas cubiertas, qué datos aporta.
- **Fuente/Medio:** tipo (web operador, directorio, prensa, video, documental, podcast, libro, red social, histórico), título, año, link, relevancia.
- **Servicio turístico:** operador, infraestructura (hotel, cabañas, spa, piscinas, pozones, tinajas, camping, restaurante, ninguna), categoría (lujo/medio/rústico/natural), temperaturas de piscina declaradas, precio, horario, contacto, redes (URL), TripAdvisor (URL, n.º opiniones, rating), Google Maps (URL, rating, reseñas), estado y fecha de verificación.
- **Barro:** nombre local, origen (volcánico, sedimentario, orgánico, salino), estado (caracterizado / declarado / informal / arcilla comercial), parámetros M (agua %, cenizas %, Cp, k, tiempo de relajación, pH, mineralogía, metales), usos ofrecidos (D), estudios.
- **Propiedad atribuida:** indicación (reumatológica, dermatológica, respiratoria, digestiva, estrés…), quién (operador D / fuente histórica / revisión clínica general), tipo de respaldo (ninguno / analogía por tipo de agua / evidencia clínica general sobre ese tipo de agua).
- **Cultura:** pueblo originario, región cultural (12 propuestas en Fase 2), toponimia (significado, lengua, fuente, nivel de confianza), uso ancestral documentado, gobernanza comunitaria (concesión, derechos de agua, centro comunitario), fuentes.

### 1.3 Formatos y construcción

- Fuente de verdad: una carpeta `data/` con CSV editables (una tabla por entidad) más `fuentes.csv`. Un script Python (`build_data.py`, evolución de `merge3.py`) valida (ids únicos, M/D presente, coordenadas dentro de Chile, fuente obligatoria), calcula los campos derivados (clase de temperatura, tipo de agua, nivel de conocimiento, completitud, nearest-hotel) y genera `site/data/termas.geojson` (ligero: lo que el mapa necesita), `site/data/termas/{id}.json` (ficha completa, carga bajo demanda) y `site/data/index.json` (búsqueda).
- Identidad: slug estable por terma; ids separados para manifestaciones (`tatio-el-jefe`), muestras (`estudio-año-nº`).
- Versionado: cada publicación de datos con número de versión y DOI en Zenodo; changelog.
- Licencia de datos: CC BY 4.0 (no NC, para que municipios y operadores puedan usarlos); fotos con licencia individual; código MIT.
- La capa Thermalia-MN del Nucleus se integra como un `estudio` más (con BioProject/ENA para secuencias) sin tocar el modelo.

---

## 2. Criterios de clasificación para las capas del mapa

Cada capa es un atributo derivado con reglas explícitas, un color o símbolo, y una leyenda con la fuente de la regla. Las capas se combinan (varias a la vez); el color del marcador lo da la capa "principal" seleccionada y las demás se expresan con forma, borde, tamaño o filtro.

| # | Capa | Regla de clasificación | Clases | Fuente de la regla |
|---|---|---|---|---|
| 1 | **Certeza / nivel de documentación** (siempre disponible, por defecto encendida) | campo `capa` | documentada · catastro/directorio · mencionada · histórica · Thermalia-MN (futura) | propia (Fase 2d) |
| 2 | **Tipo de manifestación** | `tipo_categoria` | manantial/pozón · géiser · fumarola · poza hirviente · poza de lodo · vertiente de salar · pozo | propia |
| 3 | **Origen geológico** | `origen_geologico` + dominio estructural | volcánico (arco: ZVC norte / ZVS sur) · falla Liquiñe-Ofqui (LOFS) · fallas del arco/transversales (ATF) · falla Pocuro–San Ramón / El Diablo–El Fierro (Chile central) · sedimentario/no volcánico · desconocido | Hauser 1997 (volcánico vs no volcánico); Sánchez 2013 y Wrage 2017 (LOFS vs ATF); Benavente 2015 (dominios O/C/E); Martini 2008 |
| 4 | **Temperatura** | T de la fuente (M si existe; si no, D marcada) | fría <20 °C · hipotermal 20–30 · mesotermal 30–40 · hipertermal 40–60 · muy caliente 60–85 · ebullición/vapor >85 (incluye géiseres y fumarolas) | clasificación clásica de hidrología médica (Armijo; García Matas 2006) adaptada; umbral local de ebullición en altura (Tatio 86,6 °C) |
| 5 | **Tipo de agua (química)** | aniones y cationes dominantes (meq %) sobre ternario Cl–SO₄–HCO₃ | clorurada sódica (Na-Cl) · sulfatada ácida (ácido-SO₄, pH <4) · sulfatada neutra/alcalina (Na-SO₄) · bicarbonatada (Ca/Na-HCO₃) · mixta · sin análisis | Piper/Giggenbach; nomenclatura usada en Lahsen 2005, Wrage 2017, Alvareda 2026 |
| 6 | **Mineralización** | TDS o residuo seco | oligometálica <200 mg/L · débil 200–500 · media 500–1.500 · fuerte 1.500–10.000 · salmuera >10.000 | criterio ISCIII/vademécum español y Hauser 1989 |
| 7 | **Uso: explotada vs natural** | `infraestructura` + `categoria` | centro termal con hotel/spa · piscinas o pozones habilitados · rústica (tinajas, casetas) · natural sin infraestructura · histórica/desaparecida · no apta (fumarola, ácida, hirviente) | propia, a partir de directorios y operadores |
| 8 | **Infraestructura hotelera** | servicios declarados | hotel/lodge de lujo · hotel/cabañas · camping/refugio · sin alojamiento (alojamiento más cercano en N km) | Sernatur, operadores (D) |
| 9 | **Propiedades atribuidas** | `propiedades_declaradas` + `indicaciones_historicas`, agrupadas | reumatológicas/locomotor · dermatológicas · respiratorias · digestivas/metabólicas · relajación/estrés · "curativas" sin especificar; etiqueta de respaldo: D operador / histórica / analogía por tipo de agua | operadores, Guía 1944, Domeyko; respaldo general: Cochrane 2015, Protano 2024, Cheleschi 2021, Morer 2017 |
| 10 | **Región cultural / pueblos originarios** | `region_cultural` (12) + gobernanza | aymara altiplánica · quechua-aymara de oasis · lickanantay · colla · diaguita · picunche/frontera inca · mapuche Maule-Ñuble · pewenche cordillerano · mapuche lacustre · huilliche · chono-kawésqar/colonización · patrimonio no étnico; símbolo extra: administración comunitaria confirmada | Fase 2 §6.3 |
| 11 | **Conocimiento disponible** | n.º de estudios + tesis, por tipo | sin estudios · 1–2 · 3–10 · >10; sub-capas: tiene geoquímica / tiene biología / tiene peloides / tiene isótopos | base maestra |
| 12 | **Barros** | entidad Barro | caracterizado · ofrecido sin caracterizar · informal/natural · ninguno | Fase 2 §3 |
| 13 | **Seguridad** | reglas | agua >60 °C · pH <4 · As >0,01 mg/L (norma) · accidente registrado · acceso prohibido/sensible | Tatio (As 40–50 mg/L), Baños Morales (As), Copahue, Tolhuaca, Alpehue |
| 14 | **Área protegida y volcán** | SNASPE, reserva de biósfera, volcán asociado y ranking Sernageomin 2023 | dentro de parque/reserva · zona de amortiguación · fuera; volcán ranking 1–10 | CONAF, Sernageomin |
| 15 | **Estado operativo y eventos** | últimas noticias | abierta · cerrada temporal · cerrada · en disputa · incendio/erupción reciente | prensa (Fase 2b) |
| 16 | **Histórica (1871–1972)** | registros `histórica` + indicaciones históricas | baños de Domeyko 1871 · Darapsky 1890 · Guía 1944 · Asociación 1972 | capa histórica |
| 17 | **Thermalia-MN** (futura) | sitios muestreados por el Nucleus | muestreado · con metagenoma · con aislados | Nucleus |

Reglas transversales: un marcador con dato D se dibuja con borde discontinuo; con dato M, borde continuo; "sin dato" en gris. Cada leyenda enlaza a la página "Cómo clasificamos" con la regla y la bibliografía.

---

## 3. Arquitectura de dos niveles

### 3.1 Nivel turístico/divulgativo ("Descubre")

Objetivo: que cualquier persona entienda en 30 segundos qué es la terma, dónde está, cómo es el agua y qué puede hacer allí.

Ficha turística (una pantalla, mucho aire, una foto grande):
- Nombre, nombre originario y significado (si está verificado), región/comuna, altitud, cómo llegar (texto), estado (abierta/cerrada/natural) y fecha de verificación.
- "El agua en tres datos": temperatura (icono termómetro, con M/D), tipo de agua en palabras ("clorurada sódica, como el mar diluido"), origen en una frase ("se calienta junto al volcán Casablanca").
- Qué hay: iconos de infraestructura, categoría, barros, precio orientativo, contacto, web y redes del operador, TripAdvisor/Google.
- Cultura y territorio: pueblo originario, región cultural, uso ancestral (solo si documentado), área protegida.
- "Propiedades que se le atribuyen" con la etiqueta de quién lo dice y un enlace al vademécum para "qué dice la evidencia".
- Seguridad en una línea.
- Botón "Ver la ciencia" → nivel científico; "Termas cercanas"; galería; videos/documentales.

Exploración: mapa principal con clústeres, buscador, filtros rápidos (región, categoría, temperatura, "con alojamiento", "naturales", "con barro"), rutas temáticas (Ruta del Norte/Centro/Sur, Ruta de los Géiseres, Ruta Pewenche, Ruta Histórica 1871–1944), y el juego.

### 3.2 Nivel científico ("Investiga")

Ficha científica por terma, con pestañas:
1. **Manifestaciones y muestras:** tabla de manantiales con T, pH, CE, caudal; tabla de análisis por muestra (parámetro, valor, unidad, método, fecha, estudio, M/D); descarga CSV de esa terma.
2. **Hidrogeoquímica:** diagrama ternario Cl–SO₄–HCO₃ y Piper con la terma resaltada sobre el conjunto nacional; scatter T–pH nacional con la terma resaltada (idea 1000 Springs); isótopos sobre la línea meteórica; geotermómetros reportados; origen estructural con mapa de fallas/volcanes.
3. **Biología:** comunidades reportadas (filos dominantes, taxones nuevos, enzimas/compuestos de interés), enlaces a BioProject/ENA, y "sin estudios biológicos publicados" cuando corresponda (hoy, la mayoría).
4. **Barros:** caracterización M/D y comparación con peloides de referencia (Copahue, Puyehue, Cañón del Blanco).
5. **Vademécum:** ver §4.
6. **Referencias:** estudios, tesis, documentos históricos, prensa, con tipo de dato que aporta cada uno; indicador de acceso abierto.
7. **Metadatos:** capa de certeza, completitud, fuentes de coordenadas y discrepancias, historial de cambios.

Transversal al nivel científico: página "Datos" con descarga completa (CSV, GeoJSON, JSON), diccionario de campos, DOI, licencia, y las visualizaciones nacionales (T–pH, ternario, histogramas por región, mapa de calor de conocimiento disponible, mapa de "vacíos").

### 3.3 Navegación entre niveles

Un solo URL por terma (`/termas/puyehue/`) con un conmutador "Descubre / Investiga" arriba; el estado se conserva al cambiar. En el mapa, el popup muestra los tres datos turísticos y dos botones. Bilingüe desde el inicio en la estructura (es/en), con el español como idioma de contenido; nombres originarios con su lengua.

---

## 4. El vademécum

Inspirado en el *Vademécum de aguas mineromedicinales españolas* (ISCIII) que está en la carpeta, adaptado a un contexto donde la mayoría de las termas chilenas no tienen declaración sanitaria ni ensayos clínicos propios. Es contenido de referencia: resume lo que se sabe, con fuentes, y no prescribe.

Estructura de la **ficha vademécum por terma**:
1. **Identificación:** nombre, aliases, nombre originario, ubicación, altitud, titularidad/operador, estado.
2. **Origen:** contexto geológico (volcán, falla), modelo conceptual en una frase (recarga meteórica → calentamiento → ascenso por falla), temperatura de reservorio si existe.
3. **Caracteres físicos:** temperatura (clase), caudal, aspecto (color, olor, gas, turbidez), conductividad, pH, radiactividad (hoy: "sin dato en Chile").
4. **Composición química:** tabla de iones mayores y trazas (mg/L y meq %), TDS, clasificación (tipo de agua y mineralización), elementos notables (Li, B, As, F, Si, S), comparación con aguas de referencia.
5. **Clasificación mineromedicinal** según los criterios clásicos (cloruradas, sulfatadas, bicarbonatadas, sulfuradas, ferruginosas, silíceas, litínicas, radiactivas, oligometálicas), con la advertencia de que es una clasificación por composición, no una declaración sanitaria.
6. **Propiedades y usos:** (a) lo que atribuyen operadores y guías (D); (b) lo que decían las fuentes históricas (Domeyko, Guía 1944); (c) lo que dice la evidencia general para ese tipo de agua y vía de aplicación (balneación, barro, inhalación, bebida), citando revisiones (Cochrane 2015, Protano 2024, Cheleschi 2021, Maccarone 2021, Mennuni 2021, Morer 2017, García Matas 2006, AETS 2006); (d) contraindicaciones generales; (e) seguridad del sitio.
7. **Barros:** si existen, su ficha.
8. **Biología:** síntesis.
9. **Patrimonio y cultura:** historia, uso ancestral, toponimia.
10. **Bibliografía** completa, con M/D y acceso.

Glosario transversal (término → explicación breve) enlazado desde cualquier ficha: hipertermal, clorurada sódica, meq, geotermómetro, peloide, extremófilo, sinter, LOFS, etc.

Textos generales del vademécum (páginas, no fichas): "Cómo se forma una terma", "Tipos de agua y qué significan", "Qué dice la evidencia sobre la balneoterapia" (con niveles de evidencia), "Barros termales", "Vida en el agua caliente" (microbiología termal, con los hallazgos chilenos: Porcelana, Tatio, Tinguiririca, Maule), "Seguridad en termas", "Historia del termalismo en Chile (1600–hoy)", "Termas y pueblos originarios", "Cómo clasificamos y de dónde salen los datos".

---

## 5. Juego

Dos juegos cortos (2–3 minutos), sin registro, jugables en móvil, con los mismos datos del sitio:

**"Adivina la terma".** Se muestran pistas progresivas (región borrosa → temperatura y tipo de agua → origen geológico → foto parcial → pueblo originario → dato curioso) y el jugador elige entre 4 termas en un mapa mudo; cada acierto da puntos decrecientes según las pistas usadas. Al final, ficha de la terma y "visítala". Variante infantil (kit Exploradores Termales): solo norte/centro/sur y temperatura.

**"Agua, barro y uso".** Arrastrar y soltar: tarjetas de aguas (clorurada sódica 66 °C, sulfatada ácida pH 2,4, bicarbonatada 32 °C, barro volcánico, barro salino…) a los usos de referencia (baño de inmersión, envoltura de barro, inhalación, bebida, "solo mirar: peligro") y a ejemplos de termas; cada emparejamiento explica por qué en una línea con su fuente. Enseña la diferencia entre dato medido y declarado y la seguridad.

Ambos exportables a la exposición itinerante y al kit educativo; marcadores de progreso solo en el navegador.

---

## 6. Sección de barros termales

Página propia con mapa filtrado y tres bloques:
1. **Qué es un peloide** y cómo se clasifican (natural/madurado; inorgánico/orgánico/mixto; sulfo-, filo-, salino-peloide), con la referencia de Maraver 2021 y Carretero 2020.
2. **Barros de Chile, uno por uno:** Puyehue (3 pozos, inorgánicos, caracterización física: Vela 2023), Cañón del Blanco (completo: pH 2,7, azufre, pirita, cuarzo; marca Trawe), Chillán (fango volcánico, D), Mamiña (tradicional, D), Chancho Ko (pozas de lodo ácido-sulfatadas, M parcial), Colina y Polloquere/Surire (informales), más los históricos ("baños de barro" de Río Blanco, Manzanar, Quinamávida en 1944). Estado de cada uno: caracterizado / declarado / informal.
3. **Referencia regional:** Copahue (Laguna del Chancho y Laguna Sulfurosa/Madre: azufre, pirita, hematita, cianobacterias, usos en psoriasis y artrosis) como modelo de lo que falta hacer en Chile, y un "protocolo mínimo" sugerido para caracterizar un barro (agua, cenizas, Cp, relajación, textura, mineralogía, metales, microbiología) solo como referencia conceptual.

---

## 7. Temperatura y centros turísticos en el mapa

Objetivo: que el visitante vea de un vistazo qué tan caliente es el agua de origen y dónde puede bañarse cómodamente cerca.

1. **Dos temperaturas por sitio:** temperatura de la fuente (M, borde continuo) y temperatura de uso en piscinas o pozones (D, borde discontinuo). El marcador usa un anillo de dos colores: interior = fuente, exterior = baño. Si solo hay una, el anillo es simple.
2. **Asociación manantial → centro:** para cada manifestación natural sin infraestructura se calcula el centro termal o alojamiento más cercano (distancia en línea recta y, si hay ruta conocida, en km de camino) y se dibuja como línea punteada al activar la capa "Dónde bañarse cerca". Regla: solo se asocian centros a ≤25 km o dentro de la misma comuna; se muestra la distancia y se aclara que es orientativa.
3. **Clústeres por sistema geotermal:** al alejar el zoom, las manifestaciones se agrupan por sistema (Liquiñe, Cordón Caulle, Copahue, Tatio…) y el clúster muestra el rango de temperaturas y cuántos centros con alojamiento hay.
4. **Filtro "temperatura de baño":** rango deslizante (p. ej. 36–40 °C) que resalta los centros cuyas piscinas declaradas caen en el rango, y un segundo deslizador para la temperatura de fuente.
5. **Alertas:** fuentes >60 °C, pH <4 o con arsénico alto aparecen con un símbolo de precaución aunque tengan infraestructura.

---

## 8. Arquitectura técnica y publicación en GitHub Pages

- **Sitio estático** sin servidor: HTML/CSS/JS con un generador ligero (Eleventy o Astro; alternativa mínima: páginas generadas por script Python). Mapa con **MapLibre GL** (o Leaflet si se prefiere simplicidad) y clustering; base cartográfica abierta (OpenStreetMap/OpenFreeMap) más capas de volcanes y áreas protegidas como GeoJSON.
- **Datos:** `data/*.csv` (fuente de verdad, editable) → `build_data.py` → `site/data/` (GeoJSON ligero + JSON por terma + índice de búsqueda). Validación automática en cada push (GitHub Actions): esquema, ids, coordenadas, M/D, fuentes.
- **Visualizaciones:** D3 o Plotly para ternario, Piper, T–pH y radar de barros; gráficos pequeños en SVG inline.
- **Búsqueda:** índice precomputado (Lunr/Fuse) en el cliente.
- **Estructura del repositorio** `fissotta/thermalia`:
  ```
  README.md · LICENSE (MIT) · DATA_LICENSE (CC BY 4.0) · CITATION.cff
  data/            termas.csv manifestaciones.csv muestras.csv analisis.csv estudios.csv fuentes.csv
                   servicios.csv barros.csv propiedades.csv cultura.csv medios.csv tesis.csv eventos.csv
                   diccionario.md CHANGELOG.md
  scripts/         build_data.py validate.py merge_*.py (los de la Fase 2) utm.py
  site/            src/ (páginas, componentes), public/data/ (generados), public/img/
  docs/            plan (este documento), fases 1–2, cómo contribuir, cómo clasificamos
  .github/workflows/ build-and-deploy.yml (valida, construye, publica en gh-pages)
  ```
- **Referencia técnica revisada: Terraink** (github.com/yousifamanuel/terraink, 4,1k estrellas; React + Vite + MapLibre GL + teselas vectoriales de OpenFreeMap/OpenMapTiles + Nominatim). Confirma que la pila elegida funciona sin servidor ni clave de API: OpenFreeMap sirve teselas vectoriales gratuitas de todo el planeta, y el estilo del mapa se genera en código (`maplibreStyle.ts`) a partir de un "tema" con colores por capa (tierra, cobertura, agua, cursos de agua, parques, edificios, cuatro jerarquías de caminos, ferrocarril) y anchos por nivel de zoom, exactamente el mecanismo que Thermalia necesita para un tema por zona (altiplano, desierto, bosque, estepa) y para que ríos, lagos, caminos y localidades aparezcan con detalle progresivo. Se adoptan de ahí tres ideas: (1) la **generación de estilo MapLibre desde una paleta por capa** (temas en JSON); (2) la **geocodificación con Nominatim** para el buscador; (3) la **exportación a PNG/SVG/PDF** como función "póster de tu zona termal", útil para la exposición itinerante y las escuelas. No se adopta su código: desde abril de 2026 está bajo AGPL-3.0 (copyleft, obligaría a publicar Thermalia bajo la misma licencia) y tiene marca registrada; la versión anterior es MIT pero tampoco hace falta copiarla, porque lo valioso es el enfoque y la documentación de las capas de OpenMapTiles. Terraink no tiene relieve, animación, ni fichas; es un generador de pósters estáticos.
- **Publicación:** GitHub Pages desde la rama `gh-pages` generada por la acción; dominio propio opcional después. Rendimiento: GeoJSON de mapa <1 MB (solo id, nombre, lat/lon, campos de capas); fichas cargan bajo demanda.
- **Accesibilidad y móvil:** diseño móvil primero, contraste AA, teclado, textos alternativos; modo claro/oscuro.
- **Contribución:** issues con plantilla "corregir dato" y "proponer terma"; formulario que genera un issue; revisión manual antes de incorporar.
- **Fotos:** solo con licencia (Wikimedia Commons, Flickr CC, fotos propias del Nucleus y de operadores con permiso); nunca capturas de Google. **Google Maps en la ficha:** cada terma tiene botones «Street View» (abre el panorama del punto; en producción se consulta primero la Street View Metadata API con clave gratuita para saber si existe panorama a <100 m y, si no, el botón cambia a «Satélite»), «Satélite» (Google Maps en vista satelital centrada y con zoom 16–17) y «Fotos en Google Maps» (abre la ficha del lugar con sus fotos). Las fotos de Google no se descargan ni se guardan (las condiciones de Google lo prohíben); si se quiere mostrarlas dentro del sitio, se usa la Places Photos API con clave, atribución y carga en vivo. Alternativa sin clave: incrustar Street View y satélite con el Maps Embed API (gratuito con clave) dentro de la ficha.

---

## 9. Hoja de ruta propuesta (para conversar)

| Sprint | Entrega | Depende de |
|---|---|---|
| 0 | Completar datos desde el notebook: pasada Google Maps (coordenadas exactas, rating, reseñas de ~130 termas), capa Sernageomin, tablas de Benavente 2016 / Ruiz 2015 / Negri 2017 / Risacher 1999; copiar todo a la carpeta | computador conectado |
| 1 | Repositorio inicial: estructura, licencias, datos v1 (CSV por entidad), script de construcción y validación, GitHub Action; README | — |
| 2 | Mapa mínimo publicado en Pages: clústeres, capa de certeza, tipo, temperatura, búsqueda, popup con 3 datos y enlace a ficha | sprint 1 |
| 3 | Fichas turísticas de las ~130 termas visitables (texto breve + datos + redes) y fichas de catastro para el resto | sprint 2 |
| 4 | Nivel científico: tablas de análisis, ternario/Piper, T–pH, referencias; página Datos con descarga y DOI | sprint 3 |
| 5 | Capas 3–16 completas con leyendas y página "Cómo clasificamos"; capa cultural con las 12 regiones | sprint 4 |
| 6 | Vademécum: 20 fichas completas (prioritarias + las mejor documentadas) y páginas generales; glosario | sprint 4 |
| 7 | Barros, juego, rutas temáticas, bilingüe | sprint 5–6 |
| 8 | Integración Thermalia-MN (~100 sitios), índice de valor ecológico/singularidad, versión 1.0 | datos del Nucleus |

Primer prototipo visible (sprints 1–2) es alcanzable en pocos días de trabajo una vez acordado el plan.

---

## 9b. El "mapa vivo": experiencia inmersiva (añadido 22-10-2026)

Thermalia no se abre como un mapa de puntos sino como **Chile visto desde arriba, vivo**: el territorio respira con su clima real, su hora real y sus habitantes (animales, plantas, gente), y el visitante baja suavemente de todo el país a una zona y de ahí a cada terma. Todo lo animado es sobrio, apagable y de bajo consumo; todo lo informativo es real y con fuente.

### 9b.1 Navegación por zonas y transiciones

- **Vista 0 – Chile completo:** el país entero, silueta y relieve suaves, con los clústeres de termas como brillos cálidos; sobre cada **zona** (no región administrativa) una etiqueta discreta. Al pasar el cursor, la zona se ilumina y suenan dos segundos de su ambiente.
- **Vista 1 – Zona:** al pinchar, la cámara desciende con una transición suave (1–1,5 s, easing) hasta la zona: aparece el paisaje animado de esa zona (ver 9b.2), sus ríos, lagos, volcanes y salares, y los sitios termales como puntos con su anillo de temperatura. Un panel lateral breve cuenta la zona en tres frases (geología, cultura, clima de hoy).
- **Vista 2 – Terma:** al pinchar un sitio, la cámara se acerca y se abre la ficha (Descubre/Investiga). Los paisajes y sonidos siguen de fondo, atenuados.
- Las ocho zonas propuestas, definidas por geografía y cultura y no por regiones: **Altiplano y precordillera aymara** (Arica–Tarapacá alta), **Desierto y oasis** (Pampa del Tamarugal, Atacama, Alto Loa, salares), **Puna lickanantay y volcanes del norte** (San Pedro, Tatio, Láscar, Lastarria, Ojos del Salado), **Norte Chico** (Copiapó–Choapa), **Chile central y Cordillera** (Aconcagua–Maule, fallas Pocuro y volcanes centrales), **Ñuble, Biobío y Araucanía andina** (Chillán, Alto Biobío pewenche, Lonquimay, Villarrica), **Zona lacustre y Patagonia norte** (Los Ríos, Los Lagos, fiordo Comau, Puyehue), **Aysén y Magallanes** (Puyuhuapi, Aysén, Skyring). Dentro de cada zona, los **pisos altitudinales** (costa/valle, precordillera, cordillera, altiplano/altas cumbres) cambian qué especies y gente aparecen.

### 9b.2 Habitantes del paisaje por zona y piso (especies reales; las listas son de referencia y se citan en el sitio)

| Zona | Animales (día) | Animales (noche) | Plantas y paisaje | Gente y cultura (con respeto, sin caricatura) |
|---|---|---|---|---|
| Altiplano aymara | vicuña, llama y alpaca en rebaño, flamenco andino en lagunas, suri (ñandú andino), vizcacha, tagua gigante | zorro culpeo, búho tucúquere, chinchilla de cola corta | llareta, queñoa, paja brava, bofedales; nieve en cumbres | pastores aymaras con llamas, ch'alla a la Pachamama (si se documenta), pueblos de adobe |
| Desierto y oasis | guanaco, lagartijas, colibrí del norte en oasis | murciélagos, zorro chilla | tamarugo, chañar, flor del desierto (en años lluviosos), salares con flamencos | agricultores de oasis (Pica, Mamiña), pirquineros |
| Puna lickanantay | vicuña, flamenco de James, gaviota andina, cóndor en vuelo alto | zorro culpeo, vizcacha | tola, coirón, géiseres con vapor que cambia con la hora | comunidades atacameñas (Toconce, Caspana), caravanas de llamas, patrimonio inca |
| Norte Chico | guanaco, cóndor, chinchilla (reserva Las Chinchillas), colibríes | zorro, gato colocolo | cactus candelabro, desierto florido estacional | crianceros de cabras, diaguitas del Limarí |
| Chile central y Cordillera | cóndor, águila, loica, tórtola, abejas y mariposas en valles; guanaco en altura | zorro culpeo, degú, lechuza | espino, quillay, peumo, litre; viñas; nieve y ríos de deshielo | huasos y arrieros, pueblos de campo |
| Ñuble–Biobío–Araucanía | pudú, huemul (Nevados de Chillán), carpintero negro, chucao, loro choroy, abejas | zorro chilla, monito del monte, puma (raro) | araucaria/pehuén, coigüe, lenga, copihue, ñirre; volcanes activos con fumarola | comunidades pewenche (recolección de piñones), mapuche (ruka, rewe), colonos |
| Lacustre y Patagonia norte | huillín, martín pescador, bandurria, cisne de cuello negro, chucao | monito del monte, gato güiña, murciélagos, luciérnagas | alerce, canelo, ulmo, nalca, helechos; lluvia frecuente; fiordos | huilliche, pescadores y colonos, lancheros del Comau |
| Aysén y Magallanes | huemul, ñandú patagónico, cóndor, ovejas en manadas, delfines en fiordos | zorro culpeo, puma, chuncho | lenga, ñirre, coirón, turberas, glaciares | gauchos y baqueanos, colonos sudetes y chilotes, kawésqar |

Reglas: las apariciones son **aleatorias y escasas** (una manada cada 1–3 minutos, un ave cada 20–60 s, insectos solo en primer plano y en verano), coherentes con la zona, el piso, la estación y la hora; nunca tapan información; se pueden apagar con un botón "modo sereno" y respetan `prefers-reduced-motion`.

### 9b.3 Clima real

- Cada zona consulta cada 30 minutos un pronóstico abierto sin clave (p. ej. **Open-Meteo**, que entrega estado actual, nubosidad, lluvia, nieve, viento y temperatura para una coordenada). Con eso el paisaje muestra sol, nubes que cruzan, lluvia o nieve suaves, viento en pastos y árboles, bruma en fiordos; se muestra el dato real ("Puyehue: 11 °C, lluvia ligera") con la fuente.
- Si no hay conexión, se usa el clima típico de la estación y se indica.

### 9b.4 Ciclo circadiano real

- La luz del mapa sigue la **hora solar real de cada zona** (amanecer, día, atardecer, noche; calculable en el navegador por latitud y fecha), con cielos y sombras que cambian gradualmente; un botón **"siempre de día"** fija la luz para quien quiera ver todo claro, y otro permite "ver de noche".
- Con la noche cambian los habitantes (zorros, búhos, monito del monte, murciélagos, luciérnagas, grillos), los sonidos (grillos, chuncho, viento) y las termas se ven como vapor iluminado; de día, aves, abejas, rebaños y actividad humana.

### 9b.5 Sonido

- Sonido ambiente **suave y opcional** (silenciado hasta que la persona lo activa): agua (manantial, río, lluvia), viento, aves y animales de la zona y la hora, vapor de géiser; mezcla por capas que baja al abrir una ficha.
- Los sonidos se generan en el navegador o provienen de grabaciones con licencia abierta (CC0/CC BY, con crédito en la página de créditos); nunca música con derechos.

### 9b.6 Cómo se construye (factible y liviano)

- **Relieve real en 3D:** MapLibre GL con fuente `raster-dem` (teselas Terrarium de AWS Open Data o MapTiler) activando `terrain` con exageración 1,5–2,5× (configurable: 'relieve realista' / 'relieve dramático'), capa `hillshade` para el sombreado de laderas, cielo con `sky` y cámara inclinada (pitch 50–60°) en las transiciones; así cerros, cordillera, volcanes y valles se ven en volumen a cualquier zoom. Las termas, sprites y etiquetas se anclan a la altura del terreno. En el prototipo actual el relieve es un modelo estilizado a partir de la geografía real (crestas andinas, altiplano, Cordillera de la Costa, 44 volcanes con su altura, campos de hielo) con desplazamiento vertical exagerado, porque el visor del prototipo no puede descargar teselas.
- Mapa base MapLibre con terreno/relieve y capas propias (ríos, lagos, volcanes, salares, glaciares, áreas protegidas); una **capa de animación en canvas/WebGL** encima del mapa para sprites y partículas (clima, vapor), sincronizada con la cámara.
- Sprites e ilustraciones **originales** en estilo plano y sobrio (una paleta por zona), dibujados para el proyecto (o encargados al ilustrador de la exposición "Hot Springs in Motion"), con animaciones cortas de 4–8 cuadros; ningún personaje de terceros.
- Presupuesto de rendimiento: <60 sprites simultáneos, pausa cuando la pestaña no está visible, versión reducida en móvil y en modo sereno.
- Créditos y fuentes de las listas de especies (CONAF, Ministerio del Medio Ambiente, guías de fauna) y de la información cultural en la página "Créditos".

## 10. Decisiones tomadas (22-10-2026)

| # | Decisión | Acordado |
|---|---|---|
| 1 | Alcance geográfico | Chile + Copahue–Caviahue (Argentina) como **sistema compartido**, con marcador distinto y etiqueta "Argentina". |
| 2 | Unidad del mapa | **Un marcador por terma (sitio)**; las manifestaciones se ven dentro de la ficha y al zoom máximo. |
| 3 | Capas "mencionada" e "histórica" | **Apagadas en el nivel turístico, encendidas en el científico**; activables manualmente. |
| 4 | Propiedades declaradas | Se muestran en la ficha turística **con etiqueta "lo dice el operador" (D)** y enlace a la evidencia del vademécum. |
| 5 | Fotos | **Wikimedia Commons y Flickr con licencia CC**, con autor y licencia por foto; fotos propias del Núcleo y de operadores se suman después. |
| 6 | Idiomas | **Estructura bilingüe (es/en), contenido en español primero**; nombres originarios con su lengua y fuente. |
| 7 | Tecnología | **Astro + MapLibre GL**, sitio estático construido por GitHub Action y publicado en Pages. |
| 8 | Gobernanza | **El equipo Thermalia valida** correcciones recibidas por issues/formulario; **DOI en Zenodo** por versión; datos **CC BY 4.0**, código MIT, `CITATION.cff`. |
| 9 | Coordenadas sensibles | **Todo exacto salvo petición expresa**; el modelo conserva el campo `visibilidad` para aplicar ocultamiento cuando una comunidad o CONAF lo pida. |
| 10 | Relación con la Thermalia Database | **Este sitio es la Thermalia Database pública**: capa pública ahora, capa "Thermalia-MN" con los ~100 sitios del Núcleo al final. |

### Preguntas originales (para registro)

1. **Nombre y alcance geográfico:** solo Chile, o incluir Copahue–Caviahue (Argentina) como "sistema compartido" con marcador distinto (propuesta: sí, como referencia, marcado).
2. **Unidad del mapa:** marcador por terma (sitio) con manifestaciones dentro de la ficha (propuesta), o marcador por manifestación.
3. **Qué mostrar de las capas "mencionada" e "histórica" por defecto:** propuesta: apagadas en el nivel turístico, encendidas en el científico.
4. **Cómo tratar las propiedades medicinales declaradas por operadores:** mostrarlas con etiqueta D (propuesta) o solo en el vademécum.
5. **Fotos:** fuente y licencia; si el Nucleus aportará fotografía propia.
6. **Bilingüe desde el inicio o español primero** (propuesta: estructura bilingüe, contenido español, inglés para fichas prioritarias).
7. **Tecnología:** Astro + MapLibre (propuesta) o algo más simple (HTML + Leaflet) si lo mantendrá gente sin experiencia en frameworks.
8. **Gobernanza de datos:** quién valida correcciones de la comunidad y de los operadores; cómo se cita (CITATION.cff, DOI).
9. **Coordenadas sensibles:** ocultar o aproximar sitios en territorios indígenas o frágiles a petición de las comunidades (propuesta: campo `visibilidad` con tres niveles).
10. **Relación con la base Thermalia Database del proyecto:** si este sitio es la cara pública de esa base o un producto separado que la consume.
