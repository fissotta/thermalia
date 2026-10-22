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

def temp_num(s):
    """Temperatura numérica a partir de un campo de texto. Devuelve None cuando el campo solo
    remite a una fuente ("en Martini 2008 (tabla conocida)", "Benavente 2015 (no extraída)") y
    descarta los años de las citas para no leer "2015" como grados."""
    for seg in re.split(r'[;|]', s or ''):
        if re.search(r'tabla conocida|no extra[ií]da|sin valor|rango dominio|dominio C|^\s*en\s', seg, re.I): continue
        seg = re.sub(r"[A-ZÁÉÍÓÚ][\wáéíóúñ'\-]+(?:\s+(?:et\s+al\.?|&\s+\w+|y\s+\w+))?\s*,?\s*\(?(?:19|20)\d\d[a-z]?\)?", ' ', seg)
        seg = re.sub(r'\b(?:19|20)\d\d\b', ' ', seg)
        v = first_num(seg)
        if v is not None: return v
    return None

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
        'tm': temp_num(r['T_medida_C']), 'tms': r['T_medida_C'] or None, 'tfm': r['T_fuente_medida'] or None,
        'td': temp_num(r['T_declarada_C']), 'tds': r['T_declarada_C'] or None,
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

# ---------------------------------------------------------------------------
# Sitio de datos (/data): fichas tipo vademécum por manifestación termal
# ---------------------------------------------------------------------------
def na(x):
    x = (x or '').strip()
    return None if x.upper() in ('', 'NA', 'N/A') else x

def tds_num(*fields):
    for s in fields:
        m = re.search(r'(?:TDS|STD|residuo seco|sólidos disueltos)\s*[:≈~=]?\s*(?:de\s*)?(-?\d+(?:[.,]\d+)?)', s or '', re.I)
        if m: return num(m.group(1))
    return None

COV = [  # (id, clave i18n, función de presencia)
    ('ubic', 'cUbic', lambda r, s, c, b, x: r['lat'] is not None),
    ('tm', 'cTm', lambda r, s, c, b, x: r['tm'] is not None),
    ('td', 'cTd', lambda r, s, c, b, x: r['td'] is not None),
    ('ph', 'cPh', lambda r, s, c, b, x: r['ph'] is not None),
    ('ce', 'cCe', lambda r, s, c, b, x: r['ce'] is not None),
    ('q', 'cQ', lambda r, s, c, b, x: bool(r['q'])),
    ('ion', 'cIon', lambda r, s, c, b, x: bool(r['ion'])),
    ('tds', 'cTds', lambda r, s, c, b, x: r['tds'] is not None),
    ('iso', 'cIso', lambda r, s, c, b, x: bool(r['iso'])),
    ('as', 'cAs', lambda r, s, c, b, x: r['as_'] is not None),
    ('qd', 'cQd', lambda r, s, c, b, x: bool(r['qd'])),
    ('inf', 'cInf', lambda r, s, c, b, x: bool(r['infra'])),
    ('op', 'cOp', lambda r, s, c, b, x: bool(r['op'] or r['web'])),
    ('prop', 'cProp', lambda r, s, c, b, x: bool(r['prop'])),
    ('hist', 'cHist', lambda r, s, c, b, x: bool(r['hist'])),
    ('pue', 'cPue', lambda r, s, c, b, x: bool(r['pueblo'])),
    ('bar', 'cBar', lambda r, s, c, b, x: bool(r['barros']) and r['barros'] != 'no'),
    ('seg', 'cSeg', lambda r, s, c, b, x: bool(r['seg'])),
    ('est', 'cEst', lambda r, s, c, b, x: bool(r['refE'])),
    ('tes', 'cTes', lambda r, s, c, b, x: bool(r['refT'])),
    ('med', 'cMed', lambda r, s, c, b, x: bool(r['refM'])),
]

def clase_t(x): return None if x is None else 'fría' if x < 20 else 'hipotermal' if x < 30 else 'mesotermal' if x < 40 else 'hipertermal'
def clase_m(x): return None if x is None else 'oligometálica' if x < 100 else 'débil' if x < 250 else 'media' if x < 1000 else 'fuerte'

data_out = []
for r, rec in zip(termas, out):
    rid = r['id']; s = serv.get(rid, {}); c = cult.get(rid, {}); b = barros.get(rid, {})
    tds = tds_num(r['iones_resumen'], r['tipo_quimico'], r['notas'])
    d = {
        'id': rid, 'n': r['nombre'], 'alias': na(r['alias']), 'reg': r['region'], 'com': na(r['comuna']),
        'lat': rec['lat'], 'lon': rec['lon'], 'prec': na(r['precision_coord']), 'fcoord': na(r['fuente_coord']), 'alt': na(r['altitud_m']),
        'tipo': na(r['tipo_categoria']), 'tipom': na(r['tipo_manifestacion']), 'orig': na(r['origen_geologico']), 'est': na(r['estado']), 'ap': na(r['area_protegida']), 'capa': r['capa'],
        'tm': rec['tm'], 'tms': na(r['T_medida_C']), 'tfm': na(r['T_fuente_medida']),
        'td': rec['td'], 'tds_': na(r['T_declarada_C']), 'tfd': na(r['T_fuente_declarada']),
        'th': temp_num(r['T_historica_C']), 'ths': na(r['T_historica_C']), 'tfh': na(r['T_fuente_historica']),
        'ph': rec['ph'], 'phs': na(r['pH']), 'ce': na(r['CE_uS_cm']), 'tds': tds, 'tdss': (str(int(tds)) if tds is not None and tds == int(tds) else (str(tds) if tds is not None else None)),
        'qd': na(r['caudal_L_s']), 'as_': na(r['As_mg_L']),
        'q': na(r['tipo_quimico']), 'ion': na(r['iones_resumen']), 'iso': na(r['isotopos']),
        'cat': na(s.get('categoria')), 'infra': rec['infra'], 'op': na(s.get('operador')), 'web': na(s.get('web')), 'pre': na(s.get('precio_declarado')),
        'gm': rec['gm'], 'gr': rec['gr'], 'gn': rec['gn'],
        'barros': na(b.get('barros')), 'bard': na(b.get('barro_detalle')), 'prop': rec['prop'], 'hist': na(c.get('indicaciones_historicas')),
        'pueblo': na(c.get('pueblo_originario')), 'regc': na(c.get('region_cultural')), 'top': na(c.get('toponimia')), 'topf': na(c.get('toponimia_fuente')), 'uso': na(c.get('uso_ancestral')), 'seg': na(r['seguridad']),
        'refE': rec['refE'], 'refT': rec['refT'], 'refM': rec['refM'], 'refF': rec['refF'], 'notas': na(r['notas']),
    }
    d['has'] = [cid for cid, _, f in COV if f(d, s, c, b, rec)]
    d['cmpN'] = len(d['has']); d['cmpT'] = len(COV); d['cmp'] = round(len(d['has']) / len(COV), 3)
    d['idx'] = ' '.join(filter(None, [d['n'], d['alias'], d['reg'], d['com'], d['pueblo'], d['q'], d['tipo'], d['orig']]))
    data_out.append(d)

def count(keyf):
    from collections import Counter
    return dict(Counter(k for k in (keyf(d) for d in data_out) if k))
payload = {
    'termas': data_out,
    'cov': [{'id': cid, 'k': k, 'n': sum(1 for d in data_out if cid in d['has'])} for cid, k, _ in COV],
    'dist': {'temp': count(lambda d: clase_t(d['tm'] if d['tm'] is not None else d['td'])), 'min': count(lambda d: clase_m(d['tds'])),
             'capa': count(lambda d: d['capa']), 'cat': count(lambda d: d['cat'])},
    'kpi': {'n': len(data_out), 'doc': sum(1 for d in data_out if d['capa'] == 'documentada'), 'reg': len({d['reg'] for d in data_out}),
            'tm': sum(1 for d in data_out if d['tm'] is not None), 'refs': sum(1 for d in data_out for k in ('refE', 'refT', 'refM') for x in d[k] if x[3]) + sum(len(d['refF']) for d in data_out)},
}
tpl2 = open(os.path.join(S, '_data_template.html'), encoding='utf8').read()
os.makedirs(os.path.join(S, 'data'), exist_ok=True)
open(os.path.join(S, 'data', 'index.html'), 'w', encoding='utf8').write(tpl2.replace('__DATA__', json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')))
print('OK site/data/index.html:', len(data_out), 'fichas;', 'cobertura:', ', '.join(f"{c['id']}={c['n']}" for c in payload['cov']))
