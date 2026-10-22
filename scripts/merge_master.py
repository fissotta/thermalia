import json, re, unicodedata, math, csv, collections

def load(f): return [json.loads(l) for l in open(f, encoding='utf8') if l.strip()]
gaz = load('gazetteer.jsonl'); nc = load('fichas_norte_centro.jsonl'); sa = load('fichas_sur_austral.jsonl')
tesis = load('tesis.jsonl'); medios = load('medios.jsonl')

STOP = {'termas','terma','banos','bano','de','del','la','las','los','el','y','hotel','spa','resort','eco','lodge','wellness','thermal','hot','springs','aguas','termales','naturales','parque','termal','centro','refugio','geiser','geyser','fuente','mineral'}
def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    s = re.sub(r'[^a-z0-9 ]+',' ', s)
    toks = [t for t in s.split() if t not in STOP]
    return ' '.join(toks)

def num(x):
    try:
        if x in (None,'NA','', '-'): return None
        return float(x)
    except: return None

def dist_km(a,b):
    la1,lo1,la2,lo2 = map(math.radians,[a[0],a[1],b[0],b[1]])
    d = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 6371*2*math.asin(math.sqrt(d))

master = nc + sa
for r in master:
    r.setdefault('alias', [])
    if r['alias'] in ('NA', None): r['alias'] = []
    r['_keys'] = {norm(r['nombre'])} | {norm(a) for a in r['alias'] if a}
    r['_keys'].discard('')
    r['fuentes_coord_alt'] = []
    r['ds142'] = 'NA'

def key_match(k, keys):
    if not k: return False
    if k in keys: return True
    for kk in keys:
        if not kk: continue
        if (k in kk or kk in k) and min(len(k),len(kk)) >= 5: return True
    return False

added = 0; merged = 0
for g in gaz:
    gkeys = {norm(g['nombre'])} | {norm(a) for a in (g.get('alias') or []) if a}
    gkeys.discard('')
    glat, glon = num(g.get('lat')), num(g.get('lon'))
    best = None
    for r in master:
        if r['region'] and g.get('region') and norm(r['region']) != norm(g['region']):
            # allow region naming differences only when name matches strongly
            pass
        name_hit = any(key_match(k, r['_keys']) for k in gkeys)
        rlat, rlon = num(r.get('lat')), num(r.get('lon'))
        geo_hit = (glat is not None and rlat is not None and dist_km((glat,glon),(rlat,rlon)) < 2.5)
        if name_hit or geo_hit:
            score = (2 if name_hit else 0) + (1 if geo_hit else 0)
            if best is None or score > best[0]: best = (score, r)
    if best:
        r = best[1]; merged += 1
        for a in [g['nombre']] + (g.get('alias') or []):
            if a and norm(a) not in r['_keys'] and a != r['nombre']:
                r['alias'].append(a); r['_keys'].add(norm(a))
        if num(r.get('lat')) is None and glat is not None:
            r['lat'], r['lon'] = glat, glon
            r['precision_coord'] = g.get('precision_coord','aprox'); r['fuente_coord'] = g.get('fuente_coord','gazetteer')
        elif glat is not None:
            r['fuentes_coord_alt'].append({'lat':glat,'lon':glon,'fuente':g.get('fuente_coord','gazetteer'),'precision':g.get('precision_coord')})
        if r.get('altitud_m') in ('NA',None,'') and g.get('altitud_m') not in ('NA',None,''): r['altitud_m'] = g['altitud_m']
        if g.get('ds142_n') not in (None,'NA',''): r['ds142'] = f"DS142/2000 n.º {g['ds142_n']}"
        if r.get('tipo_manifestacion') in ('NA',None,'') and g.get('tipo_manifestacion') not in ('NA',None,''): r['tipo_manifestacion'] = g['tipo_manifestacion']
        if r.get('T_declarada_C') in ('NA',None,'') and g.get('T_declarada_C') not in ('NA',None,''): r['T_declarada_C'] = g['T_declarada_C']; r['T_fuente_declarada'] = 'gazetteer (directorio)'
        for f in g.get('fuentes') or []:
            if f not in r.get('fuentes',[]): r.setdefault('fuentes',[]).append(f)
    else:
        # new record from gazetteer with NA fields
        r = {k:'NA' for k in nc[0].keys()}
        for k in ['alias','estudios','tesis','infraestructura','redes_sociales','propiedades_declaradas','noticias','videos','fuentes']: r[k] = []
        r.update({'id': g['id'], 'nombre': g['nombre'], 'alias': g.get('alias') or [], 'region': g.get('region','NA'), 'comuna': g.get('comuna','NA'),
                  'lat': glat if glat is not None else 'NA', 'lon': glon if glon is not None else 'NA',
                  'precision_coord': g.get('precision_coord','NA'), 'fuente_coord': g.get('fuente_coord','NA'),
                  'altitud_m': g.get('altitud_m','NA'), 'tipo_manifestacion': g.get('tipo_manifestacion','NA'),
                  'T_declarada_C': g.get('T_declarada_C','NA'), 'fuentes': g.get('fuentes') or [],
                  'ds142': f"DS142/2000 n.º {g['ds142_n']}" if g.get('ds142_n') not in (None,'NA','') else 'NA',
                  'fuentes_coord_alt': [], 'notas': g.get('precision_detalle','NA') if g.get('precision_detalle') else 'Solo gazetteer (sin ficha detallada)'})
        r['_keys'] = gkeys
        master.append(r); added += 1

# dedupe inside master (fichas nc/sa overlaps, e.g. aguas calientes, rio blanco)
# keep as-is but report near-duplicates
dups = []
for i,a in enumerate(master):
    for b in master[i+1:]:
        la, lb = num(a.get('lat')), num(b.get('lat'))
        if la is not None and lb is not None and dist_km((la,num(a['lon'])),(lb,num(b['lon']))) < 0.8:
            dups.append((a['id'], b['id']))

# attach tesis
for r in master: r['tesis'] = list(r.get('tesis') or []) if isinstance(r.get('tesis'), list) else []
for t in tesis:
    names = t.get('termas') or []
    if isinstance(names, str): names = [names]
    for n in names:
        k = norm(n)
        if not k: continue
        for r in master:
            if key_match(k, r['_keys']):
                if not any(x.get('link') == t['link'] for x in r['tesis']):
                    r['tesis'].append({'autor': t['autor'], 'anio': t['anio'], 'titulo': t['titulo'], 'universidad': t['universidad'], 'link': t['link']})

# attach medios
for r in master:
    r['noticias'] = list(r.get('noticias') or []) if isinstance(r.get('noticias'), list) else []
    r['videos'] = list(r.get('videos') or []) if isinstance(r.get('videos'), list) else []
    r['redes_sociales'] = list(r.get('redes_sociales') or []) if isinstance(r.get('redes_sociales'), list) else []
    r['documentales_libros'] = []
unmatched_medios = []
for m in medios:
    k = norm(m.get('terma',''))
    if not k or k == 'general':
        unmatched_medios.append(m); continue
    hit = False
    for r in master:
        if key_match(k, r['_keys']):
            hit = True
            item = {'medio': m['medio_o_canal'], 'anio': m['anio'], 'titulo': m['titulo'], 'link': m['link']}
            if m['tipo'] == 'noticia':
                if not any(x.get('link') == m['link'] for x in r['noticias']): r['noticias'].append(item)
            elif m['tipo'] == 'video':
                if not any(x.get('link') == m['link'] for x in r['videos']): r['videos'].append({'plataforma': m['medio_o_canal'], 'titulo': m['titulo'], 'link': m['link']})
            elif m['tipo'] == 'red_social':
                if not any(x.get('url') == m['link'] for x in r['redes_sociales']): r['redes_sociales'].append({'plataforma': m['medio_o_canal'], 'url': m['link']})
            else:
                r['documentales_libros'].append({'tipo': m['tipo'], **item})
    if not hit: unmatched_medios.append(m)

# --- correcciones manuales verificadas ---
byid = {r['id']: r for r in master}
if 'termas-de-rio-blanco-curacautin' in byid:
    r = byid['termas-de-rio-blanco-curacautin']
    r['lat'] = r['lon'] = 'NA'; r['precision_coord'] = 'NA'; r['fuente_coord'] = 'NA'
    r['notas'] = (str(r.get('notas','')) + ' | Coordenadas retiradas: la fusión automática había tomado las de Río Blanco (Hualaihué, Hauser 1989); el Río Blanco de Curacautín (Wrage 2017, muestra RB) queda sin coordenada verificada.').strip(' |')
if 'termas-de-aguas-calientes-general-lagos' in byid:
    r = byid['termas-de-aguas-calientes-general-lagos']
    r['lat'] = r['lon'] = 'NA'; r['precision_coord'] = 'NA'; r['fuente_coord'] = 'NA'
    r['notas'] = (str(r.get('notas','')) + ' | Coordenadas retiradas: la fuente n.º 29 "Aguas Calientes" del D.S. 142/2000 está en Antofagasta, no en General Lagos.').strip(' |')
if 'termas-rio-liquine' in byid:
    byid['termas-rio-liquine']['fuentes_coord_alt'] = [a for a in byid['termas-rio-liquine']['fuentes_coord_alt'] if 'huilo' not in a['fuente'].lower()]
if 'termas-huilo-huilo' not in byid:
    r = {k:'NA' for k in nc[0].keys()}
    for k in ['alias','estudios','tesis','infraestructura','redes_sociales','propiedades_declaradas','noticias','videos','fuentes']: r[k] = []
    r.update({'id':'termas-huilo-huilo','nombre':'Termas Huilo Huilo','alias':['Termas de Huilo Huilo'],'region':'Los Ríos','comuna':'Panguipulli','lat':'NA','lon':'NA','precision_coord':'NA','fuente_coord':'NA',
              'infraestructura':['hotel','spa','piscinas'],'categoria':'medio','fuentes':['https://termasenchile.cl/termas/termas-huilo-huilo-116'],'fuentes_coord_alt':[{'lat':-39.7654375,'lon':-72.912543,'fuente':'termasenchile.cl (pin dudoso, muy al oeste de la Reserva Huilo Huilo)','precision':'dudosa'}],'ds142':'NA',
              'notas':'Registro creado desde gazetteer; el pin del directorio parece erróneo, coordenada pendiente.','_keys':{'huilo huilo'}})
    master.append(r)
for a,b in [('termas-quimey-co','termas-peumayen'),('termas-quimey-co','termas-pucon-indomito'),('termas-san-luis','termas-montevivo'),('termas-de-conaripe','eco-termas-pellaifa'),('termas-vergara','termas-cofre'),('termas-puerto-perez','termas-de-chilconal')]:
    for i in (a,b):
        if i in byid: byid[i]['notas'] = (str(byid[i].get('notas','')) + f' | Pin del directorio a <1 km de {b if i==a else a}: centros vecinos o pin compartido; verificar en terreno.').strip(' |')
for i in ['termas-rio-liquine','termas-manquecura','termas-punulaf','termas-rayenco','termas-carranco','termas-trafipan','termas-quilalelfu']:
    if i in byid: byid[i]['notas'] = (str(byid[i].get('notas','')) + ' | Complejo de Liquiñe: varios centros a <1 km; los pines del directorio son aproximados.').strip(' |')

# finalize
for r in master:
    r.pop('_keys', None)
    r['n_tesis'] = len(r['tesis']); r['n_noticias'] = len(r['noticias']); r['n_videos'] = len(r['videos'])
    # coverage score: non-NA fields
    core = ['lat','T_medida_C','T_declarada_C','pH','tipo_quimico','infraestructura','categoria','operador','web','barros','pueblo_originario','toponimia','estudios','tesis','noticias','videos']
    filled = 0
    for c in core:
        v = r.get(c)
        if isinstance(v, list): filled += 1 if v else 0
        elif v not in ('NA', None, '', []): filled += 1
    r['completitud'] = round(filled/len(core),2)

master.sort(key=lambda r: (num(r.get('lat')) if num(r.get('lat')) is not None else -90) * -1 if False else (r.get('region',''), r['nombre']))
# order north→south by latitude where possible
order = {'Arica y Parinacota':1,'Tarapacá':2,'Antofagasta':3,'Atacama':4,'Coquimbo':5,'Valparaíso':6,'Metropolitana':7,'Región Metropolitana':7,"O'Higgins":8,'Maule':9,'Ñuble':10,'Biobío':11,'La Araucanía':12,'Araucanía':12,'Los Ríos':13,'Los Lagos':14,'Aysén':15,'Magallanes':16}
master.sort(key=lambda r: (order.get(r.get('region'), 99), -(num(r.get('lat')) or -99)))

json.dump(master, open('termas_chile_master.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
with open('termas_chile_master.jsonl','w',encoding='utf8') as f:
    for r in master: f.write(json.dumps(r, ensure_ascii=False)+'\n')

# geojson
feats = []
for r in master:
    la, lo = num(r.get('lat')), num(r.get('lon'))
    if la is None: continue
    props = {k: v for k, v in r.items() if k not in ('lat','lon')}
    feats.append({'type':'Feature','geometry':{'type':'Point','coordinates':[lo, la]},'properties': props})
json.dump({'type':'FeatureCollection','features':feats}, open('termas_chile.geojson','w',encoding='utf8'), ensure_ascii=False)

# csv flattened
def flat(v):
    if isinstance(v, list):
        out = []
        for x in v:
            if isinstance(x, dict):
                out.append(' / '.join(str(x.get(k)) for k in ('autor','anio','titulo','plataforma','medio','url','link') if x.get(k) not in (None,'NA','')))
            else: out.append(str(x))
        return ' | '.join(out) if out else 'NA'
    if isinstance(v, dict): return json.dumps(v, ensure_ascii=False)
    return v if v not in (None,'') else 'NA'
cols = ['id','nombre','alias','region','comuna','lat','lon','precision_coord','fuente_coord','altitud_m','tipo_manifestacion','origen_geologico','T_medida_C','T_fuente_medida','T_declarada_C','T_fuente_declarada','pH','CE_uS_cm','tipo_quimico','iones_resumen','isotopos','caudal_L_s','As_mg_L','n_estudios_FQ','n_estudios_G','n_estudios_B','n_estudios_Pel','n_estudios_T','n_tesis','n_noticias','n_videos','infraestructura','categoria','estado','operador','administracion_comunitaria','web','redes_sociales','precio_declarado','barros','barro_detalle','propiedades_declaradas','indicaciones_historicas','pueblo_originario','region_cultural','toponimia','toponimia_fuente','uso_ancestral','area_protegida','seguridad','ds142','estudios','tesis','noticias','videos','documentales_libros','fuentes','notas','completitud']
with open('termas_chile_master.csv','w',encoding='utf8',newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in master: w.writerow({c: flat(r.get(c,'NA')) for c in cols})

# stats
def has(r,c):
    v=r.get(c); return (bool(v) if isinstance(v,list) else v not in ('NA',None,''))
stats = {c: sum(has(r,c) for r in master) for c in cols if c not in ('id','nombre')}
byreg = collections.Counter(r.get('region') for r in master)
print('MASTER', len(master), 'fichas', len(nc)+len(sa), 'gazetteer nuevos', added, 'fusionados', merged)
print('por region', dict(byreg))
print('cobertura', json.dumps(stats, ensure_ascii=False))
print('posibles duplicados (<0.8 km):', dups)
print('medios sin terma asignada:', len(unmatched_medios), collections.Counter(m['tipo'] for m in unmatched_medios))
json.dump({'n_master':len(master),'por_region':dict(byreg),'cobertura':stats,'duplicados':dups,'medios_generales':unmatched_medios}, open('stats.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
