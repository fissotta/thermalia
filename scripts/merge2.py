import json, csv, collections, math
def load(f): return [json.loads(l) for l in open(f, encoding='utf8') if l.strip()]
master = json.load(open('termas_chile_master.json', encoding='utf8'))
byid = {r['id']: r for r in master}
template_keys = list(master[0].keys())
def isna(v): return v in ('NA', None, '', [], {})
def num(x):
    try: return float(x)
    except: return None

# 1) nuevas manifestaciones
new = load('manifestaciones_norte.jsonl') + load('manifestaciones_centro_sur.jsonl')
added = 0
for n in new:
    if n['id'] in byid: continue
    r = {k: 'NA' for k in template_keys}
    for k in ['alias','estudios','tesis','infraestructura','redes_sociales','propiedades_declaradas','noticias','videos','fuentes','fuentes_coord_alt','documentales_libros']: r[k] = []
    for k, v in n.items():
        if k == 'uso':
            r['infraestructura'] = ['ninguna'] if v in ('natural sin uso','exploración geotérmica') else r['infraestructura']
            r['categoria'] = 'natural' if v == 'natural sin uso' else r['categoria']
            r['notas'] = (f"Uso: {v}. " + (str(n.get('notas','')) if not isna(n.get('notas')) else '')).strip()
        elif k in r or k in ('id','nombre'):
            r[k] = v if not isna(v) else r.get(k, 'NA')
    if isna(r.get('lat')): r['lat'] = r['lon'] = 'NA'
    r['ds142'] = r.get('ds142','NA') or 'NA'
    master.append(r); byid[r['id']] = r; added += 1

# 2) actualizaciones: rellenar NA; si ya hay valor, guardar en 'actualizaciones' para trazabilidad
upd = load('actualizaciones_norte.jsonl') + load('actualizaciones_centro_sur.jsonl')
applied = kept = 0; missing_ids = []
for u in upd:
    r = byid.get(u['id_existente'])
    if not r: missing_ids.append(u['id_existente']); continue
    r.setdefault('actualizaciones', [])
    for k, v in (u.get('campos_nuevos') or {}).items():
        if isna(v): continue
        if k in ('estudios','fuentes','alias','noticias','videos','tesis'):
            cur = r.get(k) if isinstance(r.get(k), list) else []
            for x in (v if isinstance(v, list) else [v]):
                key = x.get('link') if isinstance(x, dict) else x
                if not any((y.get('link') if isinstance(y, dict) else y) == key for y in cur): cur.append(x)
            r[k] = cur; applied += 1
        elif k == 'notas':
            r['notas'] = (str(r.get('notas','')) + ' | ' + str(v)).strip(' |') if not isna(r.get('notas')) else v; applied += 1
        elif isna(r.get(k)):
            r[k] = v if not isinstance(v, list) else '; '.join(map(str, v)); applied += 1
            if k == 'T_medida_C' and isna(r.get('T_fuente_medida')): r['T_fuente_medida'] = u.get('fuente','NA')
            if k == 'lat' and not isna(v):
                r['precision_coord'] = 'aprox'; r['fuente_coord'] = u.get('fuente','actualización')
        else:
            r['actualizaciones'].append({'campo': k, 'valor': v, 'fuente': u.get('fuente','NA')}); kept += 1

# 3) presencia digital
pres = load('presencia_digital.jsonl')
WRONG = {
 'termas-de-aguas-calientes-general-lagos': ['termasaguascalientes','Termas-Aguas-Calientes-Parque'],
 'termas-de-ancuaque': ['termasaguascalientes','Termas-Aguas-Calientes-Parque'],
 'termas-de-chillan': ['termasaguascalientes','Termas-Aguas-Calientes-Parque'],
 'aguas-calientes-nevados-de-chillan': ['termasaguascalientes','Termas-Aguas-Calientes-Parque'],
 'termas-de-colina-colina': ['valledecolina'],
 'termas-ventisquero-puyuhuapi': ['puyuhuapilodge'],
 'termas-rio-liquine': ['tiktok.com/discover'],
 'termas-de-conaripe': ['pellaifa'],
}
for rid, bad in WRONG.items():
    r = byid.get(rid)
    if not r: continue
    r['redes_sociales'] = [x for x in r.get('redes_sociales', []) if not any(b.lower() in str(x.get('url','')).lower() for b in bad)]
    if rid == 'termas-de-conaripe': r['alias'] = [a for a in r.get('alias', []) if 'pellaifa' not in a.lower()]
    if rid == 'termas-rio-liquine':
        r['alias'] = [a for a in r.get('alias', []) if not any(s in a.lower() for s in ['rayenco','carranco','punulaf','manquecura','trafip','quilalelfu','huilo'])]
    r['notas'] = (str(r.get('notas','')) + ' | Redes cruzadas de otra terma eliminadas (revisión 21-10-2026).').strip(' |')
pres_applied = 0
for p in pres:
    r = byid.get(p['id_existente'])
    if not r: continue
    pres_applied += 1
    rs = r.get('redes_sociales') if isinstance(r.get('redes_sociales'), list) else []
    for plat in ['instagram','facebook','tiktok','youtube']:
        url = p.get(plat)
        if not isna(url) and not any(str(url).rstrip('/') == str(x.get('url','')).rstrip('/') for x in rs):
            rs.append({'plataforma': plat.capitalize(), 'url': url})
    r['redes_sociales'] = rs
    r['tripadvisor'] = {'url': p.get('tripadvisor_url','NA'), 'opiniones': p.get('tripadvisor_opiniones','NA')} if not isna(p.get('tripadvisor_url')) else 'NA'
    r['google_maps'] = {'url': p.get('google_maps_url','NA'), 'lat': p.get('google_maps_lat','NA'), 'lon': p.get('google_maps_lon','NA'), 'rating': p.get('google_rating','NA'), 'resenas': p.get('google_reseñas','NA')} if not isna(p.get('google_maps_url')) else 'NA'
    if isna(r.get('web')) and not isna(p.get('web_operador')): r['web'] = p['web_operador']
    r['contacto_reservas'] = p.get('whatsapp_o_reservas','NA')
    r['reservas_terceros'] = p.get('booking_u_otros','NA')
    if not isna(p.get('estado_operativo_segun_redes')) and p['estado_operativo_segun_redes'] != 'desconocido':
        r['estado'] = p['estado_operativo_segun_redes'] + ' (según web/redes, 21-10-2026)'
    if not isna(p.get('notas')): r['notas'] = (str(r.get('notas','')) + ' | ' + p['notas']).strip(' |')
    for f in (p.get('fuentes') or []):
        if isinstance(f, str) and f not in r.get('fuentes', []): r.setdefault('fuentes', []).append(f)
    if isna(r.get('google_maps')) and not isna(p.get('google_maps_lat')) and isna(r.get('lat')):
        r['lat'], r['lon'] = p['google_maps_lat'], p['google_maps_lon']; r['precision_coord'] = 'exacta'; r['fuente_coord'] = p['google_maps_url']

# 4) normalizar tipo_manifestacion en categorías
def tipo_cat(t):
    t = str(t).lower()
    if 'géiser' in t or 'geiser' in t or 'geyser' in t: return 'géiser'
    if 'fumarola' in t: return 'fumarola'
    if 'lodo' in t or 'barro' in t: return 'poza de lodo'
    if 'hirviente' in t or 'burbuj' in t: return 'poza hirviente'
    if 'salar' in t: return 'vertiente de salar'
    if 'pozo' in t and 'pozón' not in t and 'pozon' not in t: return 'pozo'
    if 'manantial' in t or 'vertiente' in t or 'pozón' in t or 'pozon' in t or 'terma' in t or 'baño' in t or 'laguna' in t: return 'manantial/pozón'
    return 'NA'
for r in master:
    r['tipo_categoria'] = tipo_cat(r.get('tipo_manifestacion','NA'))
    r['n_tesis'] = len(r.get('tesis') or []); r['n_noticias'] = len(r.get('noticias') or []); r['n_videos'] = len(r.get('videos') or [])
    core = ['lat','T_medida_C','T_declarada_C','pH','tipo_quimico','infraestructura','categoria','operador','web','barros','pueblo_originario','toponimia','estudios','tesis','noticias','videos','redes_sociales','tripadvisor']
    filled = sum(1 for c in core if not isna(r.get(c)))
    r['completitud'] = round(filled/len(core), 2)

order = {'Arica y Parinacota':1,'Tarapacá':2,'Antofagasta':3,'Atacama':4,'Coquimbo':5,'Valparaíso':6,'Metropolitana':7,"O'Higgins":8,'Maule':9,'Ñuble':10,'Biobío':11,'La Araucanía':12,'Los Ríos':13,'Los Lagos':14,'Aysén':15,'Magallanes':16}
master.sort(key=lambda r: (order.get(str(r.get('region')).split('/')[0].strip(), 99), -(num(r.get('lat')) or -99)))

json.dump(master, open('termas_chile_master.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
with open('termas_chile_master.jsonl','w',encoding='utf8') as f:
    for r in master: f.write(json.dumps(r, ensure_ascii=False)+'\n')
feats = [{'type':'Feature','geometry':{'type':'Point','coordinates':[num(r['lon']), num(r['lat'])]},'properties':{k:v for k,v in r.items() if k not in ('lat','lon')}} for r in master if num(r.get('lat')) is not None and num(r.get('lon')) is not None]
json.dump({'type':'FeatureCollection','features':feats}, open('termas_chile.geojson','w',encoding='utf8'), ensure_ascii=False)
def flat(v):
    if isinstance(v, list):
        out=[]
        for x in v:
            if isinstance(x, dict): out.append(' / '.join(str(x.get(k)) for k in ('autor','anio','titulo','plataforma','medio','campo','valor','url','link') if not isna(x.get(k))))
            else: out.append(str(x))
        return ' | '.join(out) if out else 'NA'
    if isinstance(v, dict): return json.dumps(v, ensure_ascii=False)
    return 'NA' if isna(v) else v
cols = ['id','nombre','alias','region','comuna','lat','lon','precision_coord','fuente_coord','altitud_m','tipo_manifestacion','tipo_categoria','origen_geologico','T_medida_C','T_fuente_medida','T_declarada_C','T_fuente_declarada','pH','CE_uS_cm','tipo_quimico','iones_resumen','isotopos','caudal_L_s','As_mg_L','n_estudios_FQ','n_estudios_G','n_estudios_B','n_estudios_Pel','n_estudios_T','n_tesis','n_noticias','n_videos','infraestructura','categoria','estado','operador','administracion_comunitaria','web','redes_sociales','tripadvisor','google_maps','contacto_reservas','reservas_terceros','precio_declarado','barros','barro_detalle','propiedades_declaradas','indicaciones_historicas','pueblo_originario','region_cultural','toponimia','toponimia_fuente','uso_ancestral','area_protegida','seguridad','ds142','estudios','tesis','noticias','videos','documentales_libros','actualizaciones','fuentes','notas','completitud']
with open('termas_chile_master.csv','w',encoding='utf8',newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in master: w.writerow({c: flat(r.get(c,'NA')) for c in cols})
stats = {c: sum(1 for r in master if not isna(r.get(c))) for c in cols if c not in ('id','nombre')}
print('MASTER', len(master), 'nuevas', added, 'actualizaciones aplicadas', applied, 'guardadas como alternativa', kept, 'ids no encontrados', missing_ids, 'presencia aplicada', pres_applied)
print('por region', dict(collections.Counter(str(r.get('region')) for r in master)))
print('por tipo', dict(collections.Counter(r['tipo_categoria'] for r in master)))
print('cobertura', json.dumps(stats, ensure_ascii=False))
print('completitud', dict(collections.Counter(round(r['completitud'],1) for r in master)))
json.dump({'n_master':len(master),'por_region':dict(collections.Counter(str(r.get('region')) for r in master)),'por_tipo':dict(collections.Counter(r['tipo_categoria'] for r in master)),'cobertura':stats}, open('stats.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
