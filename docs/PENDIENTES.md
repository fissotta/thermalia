# Pendientes para la sesión con el computador conectado

Orden sugerido (todo desde el navegador integrado o la carpeta local; nada de esto se pudo hacer desde la nube por bloqueos de red):

## 1. Copiar a la carpeta local (2 min)
- `thermalia_datos/` (base maestra v3, tesis, medios, gazetteer, scripts) → `~/proyectos/THERMALIA/thermalia_datos/`
- `thermalia_repo/` (repositorio listo para subir) → `~/proyectos/THERMALIA/thermalia_repo/`
- Documentos de fases 1–3 → `~/proyectos/THERMALIA/`

## 2. (HECHO 22-10-2026) Pasada por Google Maps (≈130 termas; `data/pendientes_googlemaps.csv`)
Para cada fila, en el navegador: buscar `consulta`, abrir el lugar, y capturar: URL canónica `/maps/place/...` (trae `@lat,lon`), rating, n.º de reseñas, horario/estado ("cerrado temporalmente"), y si existe Street View (abrir `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=lat,lon` y ver si carga panorama). Se guardan en `servicios.csv` (google_maps_url, google_rating, google_resenas) y en `termas.csv` (lat/lon con `precision_coord=exacta (Google Maps)` cuando mejore la actual). Ya probado con Chancho Ko (funciona).

## 3. Capa Sernageomin "Geoquímica de Emisiones Termales" (Araucanía–Los Lagos)
Abrir en el navegador y guardar la respuesta JSON:
`https://sdngsig.sernageomin.cl/gissdng/rest/services/RecursosEnergeticos/GeoquimicadeEmisionesTermales/MapServer/0/query?where=1%3D1&outFields=*&f=json&returnGeometry=true` (probar también capas /1 y /2). Luego cruzar por cercanía <2 km con `termas.csv` (script `scripts/merge_sernageomin.py`, por escribir) para llenar T, pH, CE, iones y coordenadas.

## 4. Tablas de tesis bloqueadas (descargar PDF y procesar con pdftotext)
- Benavente 2015 (UCh) https://repositorio.uchile.cl/handle/2250/133331 — Tabla VI‑1 (~40 manantiales Chile central)
- Ruiz Velásquez 2015 (UCh) https://repositorio.uchile.cl/handle/2250/132984 — 36 termas de Los Lagos con UTM
- Negri 2017 (UCh) https://repositorio.uchile.cl/handle/2250/151231 — 16 termas de Aysén
- Pincetti 2016 (UCh) https://repositorio.uchile.cl/handle/2250/139909 — Plomo, Morales, Colina (As)
- Sánchez‑Alfaro 2010 (UCh) https://repositorio.uchile.cl/handle/2250/103820 — 11 áreas Villarrica–Chihuío
- Celis 2012, Allende 2017, Berríos 2015, Lagos 2016, Tort 2017, Faúndes 2022 (UdeC): tablas por manantial
- Risacher, Alonso & Salazar 1999 (DGA S.I.T. 51), capítulo "Influencia del termalismo": https://horizon.documentation.ird.fr/exl-doc/pleins_textes/pleins_textes_7/divers2/010019475.pdf (si IRD vuelve a estar en línea)
- Inostroza et al. 2025 Tabla 1 (coordenadas por manantial, Atacama)
- Wrage et al. 2017 tabla completa (iones, isótopos, coordenadas de 30 termas)

## 5. Consultas Wikidata / OpenStreetMap (desde navegador)
- Overpass Turbo: `[out:json][timeout:120]; area["ISO3166-1"="CL"]->.cl; (node["natural"="hot_spring"](area.cl); node["natural"="geyser"](area.cl); node["amenity"="public_bath"]["bath:type"="hot_spring"](area.cl); node[name~"Termas|Baños|Géiser|Geyser",i](area.cl);); out body;`
- Wikidata SPARQL: instancias de Q177380 (hot spring) y Q83471 (geyser) con P17=Q298, P625, P2044.

## 6. Repositorio GitHub
- Subir `thermalia_repo/` a `github.com/fissotta/thermalia` (rama `main`), activar Pages con "GitHub Actions" como fuente. El workflow valida los CSV, construye `site/data/` y publica `site/`.
- Opcional: `git tag v0.1.0-prototipo`; registrar en Zenodo para el DOI.

## 7. Después (Sprint 2–3)
- Reemplazar el prototipo por el sitio Astro + MapLibre (terreno 3D real con Terrarium/MapTiler, OpenFreeMap, Open‑Meteo, Street View Metadata API).
- Fotos CC desde Wikimedia Commons (API) para las 130 termas visitables.
