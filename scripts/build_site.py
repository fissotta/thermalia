"""Construye site/index.html (mapa vivo) a partir de site/_template.html y los CSV de data/.
Inyecta: lista compacta de termas (con Street View, Google Maps y fotos Commons) y el contorno de Chile.
Uso: python3 scripts/build_site.py   (ejecutar después de build_data.py)
"""
import csv, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data'); S = os.path.join(ROOT, 'site')

def read(name):
    with open(os.path.join(D, name), encoding='utf8', newline='') as f:
        return list(csv.DictReader(f))

def num(x):
    try: return float(str(x).replace(',', '.'))
    except: return None

def first_num(s):
    m = re.search(r'-?\d+(?:[.,]\d+)?', s or '')
    return num(m.group(0)) if m else None

def norm(s): return re.sub(r'[^a-z0-9 ]', '', (s or '').lower().replace('ñ', 'n'))

ZONAS = [(1, -21.5, -17.5), (2, -26, -21.5), (3, -32.2, -26), (4, -36.3, -32.2), (5, -39.5, -36.3), (6, -44.5, -39.5), (7, -49, -44.5), (8, -56, -49)]
def zona(lat):
    if lat is None: return None
    for z, a, b in ZONAS:
        if a <= lat < b: return z
    return 8 if lat < -49 else 1

termas = read('termas.csv'); serv = {r['id']: r for r in read('servicios.csv')}; cult = {r['id']: r for r in read('cultura.csv')}
barros = {r['id']: r for r in read('barros.csv')}
est = {}; [est.setdefault(r['id_terma'], []).append(r) for r in read('estudios.csv')]
tesis = read('tesis.csv'); medios = read('medios.csv')
fuentes = {}; [fuentes.setdefault(r['id_terma'], []).append(r['url']) for r in read('fuentes.csv') if r.get('url')]
sv = {r['id']: r for r in read('streetview.csv')} if os.path.exists(os.path.join(D, 'streetview.csv')) else {}
fotos = json.load(open(os.path.join(D, 'fotos_commons.json'), encoding='utf8'))
fotos.pop('_meta', None)

out = []
for r in termas:
    rid = r['id']; s = serv.get(rid, {}); c = cult.get(rid, {}); b = barros.get(rid, {}); v = sv.get(rid, {})
    la, lo = num(r['lat']), num(r['lon'])
    tes_l = [t for t in tesis if norm(r['nombre']) and norm(r['nombre']) in norm(t['termas'])]
    ntes = len(tes_l)
    med_l = [m for m in medios if norm(m['terma']) and (norm(m['terma']) in norm(r['nombre']) or norm(r['nombre']) in norm(m['terma']))]
    infra = [x.strip() for x in (s.get('infraestructura') or '').split('|') if x.strip()]
    prop = [x.strip() for x in (s.get('propiedades_declaradas') or '').split('|') if x.strip()]
    gm = s.get('google_maps_url') or None
    rec = {
        'id': rid, 'n': r['nombre'], 'reg': r['region'], 'com': r['comuna'] or None, 'lat': la, 'lon': lo, 'z': zona(la),
        'capa': r['capa'], 'tipo': r['tipo_categoria'] or 'NA',
        'tm': first_num(r['T_medida_C']), 'tms': r['T_medida_C'] or None, 'tfm': r['T_fuente_medida'] or None,
        'td': first_num(r['T_declarada_C']), 'tds': r['T_declarada_C'] or None,
        'ph': first_num(r['pH']), 'q': (r['tipo_quimico'] or None), 'cat': s.get('categoria') or None,
        'infra': infra, 'pueblo': c.get('pueblo_originario') or None, 'orig': r['origen_geologico'] or None,
        'web': s.get('web') or None, 'nest': len(est.get(rid, [])), 'ntes': ntes,
        'barros': b.get('barros') or None, 'prop': prop, 'est': r['estado'] or None,
        'alt': first_num(r['altitud_m']), 'prec': r['precision_coord'] or None, 'seg': r['seguridad'] or None,
        'as': first_num(r['As_mg_L']), 'ds142': (r['ds142'] or '').strip() or None,
        'sv': ('si' if v.get('disponible', '').startswith('si') else 'cerca' if v.get('disponible', '').startswith('cerca') else None),
        'svu': v.get('url_pano') or None, 'svt': v.get('tipo') or None,
        'gm': gm, 'gr': s.get('google_rating') or None, 'gn': s.get('google_resenas') or None,
        'fot': fotos.get(rid, []),
        # referencias para el popup: [autor, año, título, enlace]
        'refE': [[e['autor'], e['anio'], e['titulo'], e['link']] for e in est.get(rid, [])],
        'refT': [[t['autor'], t['anio'], t['titulo'] + (' (' + t['universidad'] + ')' if t.get('universidad') else ''), t['link']] for t in tes_l],
        'refM': [[m['medio_o_canal'], m['anio'], m['titulo'], m['link']] for m in med_l],
        'refF': fuentes.get(rid, []),
    }
    # recortes para mantener el HTML liviano
    for k in ('q', 'orig'):
        if rec[k] and len(rec[k]) > 60: rec[k] = rec[k][:59] + '…'
    out.append(rec)

tpl = open(os.path.join(S, '_template.html'), encoding='utf8').read()
chile = open(os.path.join(S, 'data', 'chile.json'), encoding='utf8').read()
html = tpl.replace('__TERMAS__', json.dumps(out, ensure_ascii=False, separators=(',', ':'))).replace('__CHILE__', chile)
if not html.lstrip().startswith('<!doctype'):
    html = '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + html.replace('<div id="stage">', '</head>\n<body>\n<div id="stage">', 1) + '\n</body>\n</html>\n'
open(os.path.join(S, 'index.html'), 'w', encoding='utf8').write(html)
print('OK site/index.html:', len(out), 'termas;', sum(1 for r in out if r['lat'] is not None), 'con coordenadas;', sum(1 for r in out if r['sv']), 'con Street View;', sum(1 for r in out if r['fot']), 'con fotos;', sum(1 for r in out if r['gm']), 'con ficha Google Maps')
