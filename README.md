# Thermalia — Vademécum digital de las termas de Chile

Plataforma abierta de divulgación científica y turística sobre las manifestaciones termales de Chile: un mapa vivo del país con capas (certeza, tipo, temperatura, química, uso, cultura, conocimiento, barros, seguridad) y una ficha por terma con dos niveles, **Descubre** (turístico) e **Investiga** (científico, con vademécum y bibliografía). Proyecto del Núcleo Milenio de Geobiología de Ecosistemas Termales Andinos (MN‑Thermalia).

Estado: **prototipo** (octubre 2026). Base de datos pública de **303 manifestaciones termales** construida desde literatura científica, catastros oficiales, tesis, directorios turísticos, prensa y fuentes históricas. Cada dato distingue **M** (medido en estudio) de **D** (declarado por operador o guía) y lleva su fuente; `NA` donde no hay dato. Los ~100 sitios muestreados por el Núcleo se integrarán al final del proyecto como capa "Thermalia‑MN".

## Estructura

```
data/        CSV por entidad (fuente de verdad, editable) + termas_chile_master.json + diccionario.md
scripts/     build_data.py (valida y genera site/data), merge_*.py y build_gazetteer.py (reproducen la fusión)
site/        sitio estático publicado en GitHub Pages (index.html, prototipo_mapa_vivo.html, data/)
docs/        Fase 1 inventario, Fase 2 investigación, Fase 3 plan de la plataforma, README de datos
```

## Datos

- `data/termas.csv`: una fila por manifestación (id, nombre, capa de certeza, ubicación, tipo, origen, T medida/declarada/histórica, pH, química, isótopos, As, seguridad, D.S. 142/2000…).
- `data/servicios.csv`: infraestructura, operador, web, redes, TripAdvisor, Google Maps, precios, estado.
- `data/cultura.csv`: pueblo originario, región cultural, toponimia, uso ancestral, indicaciones históricas.
- `data/barros.csv`, `data/estudios.csv`, `data/tesis.csv`, `data/medios.csv`, `data/fuentes.csv`.
- `data/termas_chile_master.json`: todos los campos por registro (versión completa).
- `site/data/termas_chile.geojson`: puntos con coordenadas para el mapa.

Licencias: código **MIT** (`LICENSE`); datos **CC BY 4.0** (`DATA_LICENSE.md`). Cómo citar: `CITATION.cff`.

## Construir

```
python3 scripts/build_data.py   # valida los CSV y regenera site/data/
```
El sitio es estático; GitHub Pages publica la carpeta `site/` mediante `.github/workflows/pages.yml`.

## Contribuir
Correcciones y nuevas termas por *issues* (plantilla "corregir dato" / "proponer terma"). Toda contribución debe traer fuente y marcar M/D. El equipo Thermalia revisa antes de incorporar.
