import json, csv, collections
exec(open('merge2.py').read().split("# 1) nuevas manifestaciones")[0])  # reutiliza load/isna/num y carga master

template_keys = list(master[0].keys())
def blank(idv, nombre):
    r = {k: 'NA' for k in template_keys}
    for k in ['alias','estudios','tesis','infraestructura','redes_sociales','propiedades_declaradas','noticias','videos','fuentes','fuentes_coord_alt','documentales_libros','actualizaciones']: r[k] = []
    r['id'] = idv; r['nombre'] = nombre; return r

# 1) manifestaciones extra (documentada / mencionada)
added = 0
for n in load('manifestaciones_extra.jsonl'):
    if n['id'] in byid: continue
    r = blank(n['id'], n['nombre'])
    for k, v in n.items():
        if k == 'uso':
            if v in ('natural sin uso','exploración geotérmica'): r['infraestructura'] = ['ninguna']; r['categoria'] = 'natural'
            r['notas'] = f"Uso: {v}."
        elif k == 'nivel_documentacion': r['capa'] = v
        elif k in r or k in ('id','nombre'): r[k] = v if not isna(v) else r.get(k,'NA')
    if not isna(n.get('notas')): r['notas'] = (r.get('notas','') + ' ' + str(n['notas'])).strip()
    master.append(r); byid[r['id']] = r; added += 1

# 2) histórico
hist_added = 0
for n in load('historico.jsonl'):
    if n['id'] in byid: continue
    r = blank(n['id'], n['nombre']); r['capa'] = 'histórica'
    for k in ['alias','region','comuna','lat','lon','precision_coord','fuente_coord','altitud_m','tipo_manifestacion','fuentes','notas']:
        if not isna(n.get(k)): r[k] = n[k]
    r['T_historica_C'] = n.get('T_historica_C','NA'); r['T_fuente_historica'] = n.get('T_fuente_historica','NA')
    r['tipo_quimico'] = n.get('tipo_quimico_historico','NA')
    r['indicaciones_historicas'] = f"{n.get('fuente','')} — «{n.get('cita_breve','')}»".strip(' —«»')
    r['estado'] = f"histórico: {n.get('estado_actual','desconocido')}"
    r['origen_geologico'] = 'NA'
    master.append(r); byid[r['id']] = r; hist_added += 1

# 3) actualizaciones (extra + histórico): rellena NA; si existe, guarda alternativa
applied = kept = 0
for u in load('actualizaciones_extra.jsonl') + load('actualizaciones_historico.jsonl'):
    r = byid.get(u['id_existente'])
    if not r: print('id no encontrado', u['id_existente']); continue
    r.setdefault('actualizaciones', [])
    for k, v in (u.get('campos_nuevos') or {}).items():
        if isna(v): continue
        if k in ('estudios','fuentes','alias','noticias','videos','tesis'):
            cur = r.get(k) if isinstance(r.get(k), list) else []
            for x in (v if isinstance(v, list) else [v]):
                key = x.get('link') if isinstance(x, dict) else x
                if not any((y.get('link') if isinstance(y, dict) else y) == key for y in cur): cur.append(x)
            r[k] = cur; applied += 1
        elif k in ('notas','indicaciones_historicas','cita_breve'):
            tgt = 'indicaciones_historicas' if k == 'cita_breve' else k
            r[tgt] = (str(r.get(tgt,'')) + ' | ' + str(v)).strip(' |') if not isna(r.get(tgt)) else str(v); applied += 1
        elif k == 'fuente':
            if v not in r['fuentes']: r['fuentes'].append(v)
        elif isna(r.get(k)):
            r[k] = v if not isinstance(v, list) else '; '.join(map(str, v)); applied += 1
            if k == 'T_medida_C' and isna(r.get('T_fuente_medida')): r['T_fuente_medida'] = u.get('fuente','NA')
            if k == 'lat': r['precision_coord'] = 'aprox'; r['fuente_coord'] = u.get('fuente','actualización')
        else:
            r['actualizaciones'].append({'campo': k, 'valor': v, 'fuente': u.get('fuente','NA')}); kept += 1

# 4) alias erróneos detectados
WRONG_ALIAS = {'termas-de-chillan': ['chinchillani'], 'termas-de-catillo': ['risopatr'], 'termas-de-mamina': ['los barros','barroso'],
               'banos-de-azufre': ['sopas','venados'], 'termas-de-aguas-calientes-general-lagos': ['salar aguas calientes','antofagasta'], 'termas-el-rincon': ['rinconada']}
for rid, bad in WRONG_ALIAS.items():
    r = byid.get(rid)
    if not r: continue
    before = len(r.get('alias', []))
    r['alias'] = [a for a in r.get('alias', []) if not any(b in a.lower() for b in bad)]
    if len(r['alias']) < before: r['notas'] = (str(r.get('notas','')) + ' | Alias de otra manifestación retirado (revisión 2c).').strip(' |')
if 'termas-de-molulco' in byid: byid['termas-de-molulco']['notas'] = (str(byid['termas-de-molulco'].get('notas','')) + ' | Posible duplicado de Termas de Balboa según D.S. 142/2000 (misma zona); verificar en terreno.').strip(' |')

# 5) capa por nivel de documentación
for r in master:
    if r.get('capa') in ('mencionada','histórica','documentada'): continue
    has_data = any(not isna(r.get(k)) for k in ('T_medida_C','pH','tipo_quimico','iones_resumen')) or (r.get('estudios') or []) or (r.get('tesis') or [])
    r['capa'] = 'documentada' if has_data else 'catastro/directorio'

# 6) recomputar y exportar (misma lógica que merge2)
def tipo_cat(t):
    t = str(t).lower()
    if 'géiser' in t or 'geiser' in t or 'geyser' in t: return 'géiser'
    if 'fumarola' in t or 'solfatara' in t: return 'fumarola'
    if 'lodo' in t or 'barro' in t: return 'poza de lodo'
    if 'hirviente' in t or 'burbuj' in t: return 'poza hirviente'
    if 'salar' in t: return 'vertiente de salar'
    if 'pozo' in t and 'pozón' not in t and 'pozon' not in t: return 'pozo'
    if any(s in t for s in ['manantial','vertiente','pozón','pozon','terma','baño','laguna','agua']): return 'manantial/pozón'
    return 'NA'
for r in master:
    r['tipo_categoria'] = tipo_cat(r.get('tipo_manifestacion','NA'))
    r['n_tesis'] = len(r.get('tesis') or []); r['n_noticias'] = len(r.get('noticias') or []); r['n_videos'] = len(r.get('videos') or [])
    core = ['lat','T_medida_C','T_declarada_C','pH','tipo_quimico','infraestructura','categoria','operador','web','barros','pueblo_originario','toponimia','estudios','tesis','noticias','videos','redes_sociales','tripadvisor']
    r['completitud'] = round(sum(1 for c in core if not isna(r.get(c)))/len(core), 2)
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
cols = ['id','nombre','alias','capa','region','comuna','lat','lon','precision_coord','fuente_coord','altitud_m','tipo_manifestacion','tipo_categoria','origen_geologico','T_medida_C','T_fuente_medida','T_declarada_C','T_fuente_declarada','T_historica_C','T_fuente_historica','pH','CE_uS_cm','tipo_quimico','iones_resumen','isotopos','caudal_L_s','As_mg_L','n_estudios_FQ','n_estudios_G','n_estudios_B','n_estudios_Pel','n_estudios_T','n_tesis','n_noticias','n_videos','infraestructura','categoria','estado','operador','administracion_comunitaria','web','redes_sociales','tripadvisor','google_maps','contacto_reservas','reservas_terceros','precio_declarado','barros','barro_detalle','propiedades_declaradas','indicaciones_historicas','pueblo_originario','region_cultural','toponimia','toponimia_fuente','uso_ancestral','area_protegida','seguridad','ds142','estudios','tesis','noticias','videos','documentales_libros','actualizaciones','fuentes','notas','completitud']
with open('termas_chile_master.csv','w',encoding='utf8',newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in master: w.writerow({c: flat(r.get(c,'NA')) for c in cols})
stats = {c: sum(1 for r in master if not isna(r.get(c))) for c in cols if c not in ('id','nombre')}
print('MASTER', len(master), 'extra', added, 'histórico', hist_added, 'act aplicadas', applied, 'alternativas', kept)
print('por capa', dict(collections.Counter(r['capa'] for r in master)))
print('por region', dict(collections.Counter(str(r.get('region')) for r in master)))
print('por tipo', dict(collections.Counter(r['tipo_categoria'] for r in master)))
print('cobertura', json.dumps(stats, ensure_ascii=False))
json.dump({'n_master':len(master),'por_capa':dict(collections.Counter(r['capa'] for r in master)),'por_region':dict(collections.Counter(str(r.get('region')) for r in master)),'por_tipo':dict(collections.Counter(r['tipo_categoria'] for r in master)),'cobertura':stats}, open('stats.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
