"""Valida los CSV de data/ y regenera site/data/ (GeoJSON del mapa, índice y fichas JSON por terma).
Uso: python3 scripts/build_data.py
"""
import csv, json, os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data'); S = os.path.join(ROOT, 'site', 'data'); os.makedirs(os.path.join(S, 'termas'), exist_ok=True)

def read(name):
    with open(os.path.join(D, name), encoding='utf8', newline='') as f:
        return list(csv.DictReader(f))

def num(x):
    try: return float(x)
    except: return None

termas = read('termas.csv'); serv = {r['id']: r for r in read('servicios.csv')}; cult = {r['id']: r for r in read('cultura.csv')}
barros = {r['id']: r for r in read('barros.csv')}
est = {}; [est.setdefault(r['id_terma'], []).append(r) for r in read('estudios.csv')]
fuentes = {}; [fuentes.setdefault(r['id_terma'], []).append(r['url']) for r in read('fuentes.csv')]
tesis = read('tesis.csv'); medios = read('medios.csv')

errores = []
ids = [r['id'] for r in termas]
if len(ids) != len(set(ids)): errores.append('ids duplicados en termas.csv')
for r in termas:
    if not re.fullmatch(r'[a-z0-9-]+', r['id']): errores.append(f"id inválido: {r['id']}")
    la, lo = num(r['lat']), num(r['lon'])
    if (la is None) != (lo is None): errores.append(f"{r['id']}: lat/lon incompletos")
    if la is not None and not (-57 <= la <= -17 and -80 <= lo <= -63): errores.append(f"{r['id']}: coordenada fuera de Chile ({la},{lo})")
    if r['capa'] not in ('documentada', 'catastro/directorio', 'mencionada', 'histórica'): errores.append(f"{r['id']}: capa desconocida '{r['capa']}'")
    if r['T_medida_C'] and not r['T_fuente_medida']: errores.append(f"{r['id']}: T medida sin fuente")
if errores:
    print('ERRORES:'); [print(' -', e) for e in errores]; sys.exit(1)

def norm(s): return re.sub(r'[^a-z0-9 ]', '', s.lower().replace('ñ','n'))
feats = []; index = []
for r in termas:
    rid = r['id']; sv = serv.get(rid, {}); cu = cult.get(rid, {}); ba = barros.get(rid, {})
    ficha = {**r, 'servicios': sv, 'cultura': cu, 'barros': ba, 'estudios': est.get(rid, []), 'fuentes': fuentes.get(rid, []),
             'tesis': [t for t in tesis if norm(r['nombre']) in norm(t['termas']) or any(norm(a) and norm(a) in norm(t['termas']) for a in r['alias'].split(' | '))],
             'medios': [m for m in medios if norm(m['terma']) and (norm(m['terma']) in norm(r['nombre']) or norm(r['nombre']) in norm(m['terma']))]}
    with open(os.path.join(S, 'termas', rid + '.json'), 'w', encoding='utf8') as f: json.dump(ficha, f, ensure_ascii=False)
    la, lo = num(r['lat']), num(r['lon'])
    index.append({'id': rid, 'n': r['nombre'], 'reg': r['region'], 'capa': r['capa'], 'tipo': r['tipo_categoria']})
    if la is None: continue
    feats.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [lo, la]}, 'properties': {
        'id': rid, 'nombre': r['nombre'], 'region': r['region'], 'comuna': r['comuna'], 'capa': r['capa'], 'tipo': r['tipo_categoria'],
        'T_medida_C': r['T_medida_C'], 'T_declarada_C': r['T_declarada_C'], 'pH': r['pH'], 'tipo_quimico': r['tipo_quimico'],
        'categoria': sv.get('categoria', ''), 'infraestructura': sv.get('infraestructura', ''), 'pueblo_originario': cu.get('pueblo_originario', ''),
        'barros': ba.get('barros', ''), 'n_estudios': len(est.get(rid, [])), 'precision_coord': r['precision_coord']}})
with open(os.path.join(S, 'termas_chile.geojson'), 'w', encoding='utf8') as f: json.dump({'type': 'FeatureCollection', 'features': feats}, f, ensure_ascii=False)
with open(os.path.join(S, 'index.json'), 'w', encoding='utf8') as f: json.dump(index, f, ensure_ascii=False)
print(f'OK: {len(termas)} termas, {len(feats)} con coordenadas, {len(est)} con estudios')
