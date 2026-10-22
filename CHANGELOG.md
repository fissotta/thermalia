# Changelog

## 2026-10-22
- Mapa vivo: animaciones siempre activas (se quitó el botón "Modo sereno"); fauna y gente nacen dentro de lo que se ve en pantalla; autos (pocos, con luces de noche) circulando por las rutas; clima real por zona desde Open-Meteo (temperatura, nubes, lluvia/nieve, viento; cada 30 min, con respaldo simulado) y sol suave cuando está despejado.
- Mapa vivo: capas combinables (botones, varias a la vez) con símbolo propio por capa y color por valor; nuevas capas Barros y Seguridad; galería de fotos en la ficha (Wikimedia Commons, con autor y licencia, flechas y puntos); botones de la ficha en naranjo solo cuando hay información verificada (Street View comprobado, ficha Google Maps con rating, fotos libres, web).
- `data/streetview.csv`: disponibilidad de Street View/fotoesferas en el punto (≤50 m) o cerca (≤300 m) para las 243 termas con coordenadas (77 en el punto, 23 cerca, 143 sin cobertura), con id de panorama y enlace directo.
- `data/fotos_commons.json`: 60 termas con fotos libres de Commons (curado a mano; se distingue foto de la terma vs. entorno < 1 km).
- `scripts/build_site.py`: genera `site/index.html` desde `site/_template.html` + CSV (ejecutar tras `build_data.py`).
- Pasada por Google Maps de las 189 manifestaciones pendientes (`data/google_maps_resultados.csv`): 124 fichas encontradas, 35 sin ficha, 29 homónimos descartados, 1 por verificar (Skyring).
- `servicios.csv`: 97 URLs canónicas de Google Maps nuevas, con rating, n° de reseñas, teléfono y web (etiquetados "Google Maps", dato declarado D).
- `termas.csv`: 94 coordenadas pasadas a "exacta (Google Maps)"; corregidas coordenadas previas erróneas de Termas Valle Hermoso y Termas Cañón del Blanco.
- Regla aplicada: las fichas de Google que corresponden al volcán (cumbre) no sustituyen la coordenada de fumarolas; se registran solo en `google_maps_resultados.csv`.

## 0.1.0-prototipo (2026-10-22)
- Base maestra de 303 manifestaciones termales (capas documentada / catastro / mencionada / histórica).
- 111 tesis, 218 ítems de prensa, video y redes; presencia digital de 98 termas.
- Prototipo "mapa vivo" (relieve estilizado, zonas, capas, hora solar real, clima simulado, fauna, sonido y música generativa).
- Documentos de Fase 1, 2 y 3.
