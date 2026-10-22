import json, re, unicodedata

FIELDS = ["id","nombre","alias","region","comuna","lat","lon","precision_coord","fuente_coord","altitud_m","tipo_manifestacion","origen_geologico","T_medida_C","T_fuente_medida","T_declarada_C","T_fuente_declarada","pH","CE_uS_cm","tipo_quimico","iones_resumen","isotopos","caudal_L_s","As_mg_L","n_estudios_FQ","n_estudios_G","n_estudios_B","n_estudios_Pel","n_estudios_T","estudios","tesis","infraestructura","categoria","estado","operador","administracion_comunitaria","web","redes_sociales","precio_declarado","barros","barro_detalle","propiedades_declaradas","indicaciones_historicas","pueblo_originario","region_cultural","toponimia","toponimia_fuente","uso_ancestral","noticias","videos","area_protegida","seguridad","fuentes","notas"]
LIST_FIELDS = {"alias","estudios","tesis","infraestructura","redes_sociales","propiedades_declaradas","noticias","videos","fuentes"}

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+","-",s).strip("-").lower()
    return s

# ---- fuentes reutilizables
U_WRAGE="https://www.academia.edu/63275479/Geochemistry_of_thermal_waters_in_the_Southern_Volcanic_Zone_Chile_Implications_for_structural_controls_on_geothermal_fluid_composition"
U_ALAM="https://cec.uchile.cl/~ayaz/grc.pdf"
U_SANCHEZ="https://cec.uchile.cl/~ayaz/cgc2009b.pdf"
U_MUNOZ="https://www.cec.uchile.cl/~ayaz/grc35.pdf"
U_HAUSER="https://www.andeangeology.cl/index.php/revista1/article/download/V16n2-a06/pdf"
U_NEGRI="https://doi.org/10.1016/J.GEXPLO.2017.10.026"
U_BERRIOS="https://repositorio.uchile.cl/handle/2250/134130"
U_CELIS="https://repositorio.uchile.cl/handle/2250/111537"
U_ALLENDE="https://repositorio.uchile.cl/handle/2250/144311"
U_NEGRIT="https://repositorio.uchile.cl/handle/2250/151231"
U_GAVIRIA="https://iris.unipa.it/retrieve/e3ad8919-9a4b-da0e-e053-3705fe0a2b96/Gavira%20et%20al.%2c%202016%20def.pdf"
U_MDPI="https://www2.mdpi.com/2076-2607/3/3/344"
U_ALPEHUE="https://repositorio.uchile.cl/handle/2250/179586"
U_PEREZ="https://repositorio.uchile.cl/handle/2250/173810"
U_FELIU="https://repositorio.uchile.cl/handle/2250/115911"
U_TEC="https://www.termasenchile.cl/termas/"
U_SERN_IX="https://www.sernatur.cl/wp-content/uploads/2018/09/IX-REGION-DE-LA-ARAUCANIA.pdf"
U_SERN_XIV="https://www.sernatur.cl/wp-content/uploads/2018/09/XIV-REGION-DE-LOS-RIOS.pdf"
U_SERN_X="https://www.sernatur.cl/wp-content/uploads/2018/09/X-REGION-DE-LOS-LAGOS.pdf"
U_SERN_VIII="https://www.sernatur.cl/wp-content/uploads/2018/09/VIII-REGION-DEL-BIOBIO.pdf"
U_SITRURAL_AB="https://www.sitrural.cl/wp-content/uploads/2020/03/AltoBioBio_turismo.pdf"
U_DIARIOC="https://assets.diarioconcepcion.cl/2019/06/EE-Turismo-Invierno-15-06-2019.pdf"
U_METEO_MAL="https://www.meteored.cl/noticias/ocio/cuatro-termas-para-visitar-desde-malalcahuello-descanso-y-relajacion-en-la-araucania-andina.html"
U_METEO_PUC="https://www.meteored.cl/noticias/ocio/las-5-mejores-termas-para-visitar-desde-pucon-descanso-y-relajacion-en-el-sur-de-chile.html"
U_CT_PUCON="https://chile.travel/blog/termas-de-pucon-conoce-la-ciudad-mas-termal-de-chile/"
U_CT_2026="https://chile.travel/?p=103409"
U_CT_AUSTRAL="https://chile.travel/blog/las-6-mejores-termas-de-la-carretera-austral-segun-chile-travel/"
U_NOMADES="https://www.nomades.com/blog/las-10-mejores-termas-rusticas-naturales-chile/"
U_ELMOS_RIOS="https://www.elmostrador.cl/cultura/2014/06/23/la-indomable-belleza-de-la-ruta-termal-en-el-corazon-de-la-region-de-los-rios/"
U_ELMOS_SOL="https://www.elmostrador.cl/generacion-m/2020/03/13/abre-el-primer-centro-termal-de-puelo-termas-del-sol"
U_MUNI_AB="https://munialtobiobio.cl/turismo/donde-ir/"
U_CEQUA="https://www.cequa.cl/wp-content/uploads/2021/04/08.pdf"

WRAGE={"autor":"Wrage, J.; Tardani, D.; Reich, M.; Daniele, L.; Arancibia, G.; Cembrano, J.; Sánchez-Alfaro, P.; Morata, D.; Pérez-Moreno, R.","anio":2017,"titulo":"Geochemistry of thermal waters in the Southern Volcanic Zone, Chile – Implications for structural controls on geothermal fluid composition (Chemical Geology 466:545-561)","tipo":"FQ","link":U_WRAGE}
ALAM={"autor":"Alam, M.A.; Sánchez, P.; Parada, M.A.","anio":2010,"titulo":"Interplay of volcanism and structural control in defining the geothermal system(s) along the Liquiñe-Ofqui Fault Zone, south-central Chile (GRC Transactions 34)","tipo":"FQ","link":U_ALAM}
SANCHEZ={"autor":"Sánchez, P.; Alam, M.A.","anio":2009,"titulo":"Rol de las distintas fuentes de calor en las aguas termales del área Villarrica-Chihuio, sur de Chile (XII Congreso Geológico Chileno)","tipo":"FQ","link":U_SANCHEZ}
MUNOZ={"autor":"Muñoz, M.; Alam, M.A.; Parada, M.A.; Lahsen, A.","anio":2011,"titulo":"Geothermal system associated with the Sierra Nevada volcano, Araucanía Region, Chile (GRC Transactions 35:935-942)","tipo":"FQ","link":U_MUNOZ}
HAUSER={"autor":"Hauser, A.","anio":1989,"titulo":"Fuentes termales y minerales en torno a la Carretera Austral, Regiones X-XI, Chile (Revista Geológica de Chile 16(2):229-239)","tipo":"FQ","link":U_HAUSER}
NEGRI={"autor":"Negri, A.; Daniele, L.; Aravena, D.; Muñoz, M.; Delgado, A.; Morata, D.","anio":2018,"titulo":"Decoding fjord water contribution and geochemical processes in the Aysen thermal springs (J. Geochem. Explor. 185:1-13)","tipo":"FQ","link":U_NEGRI}
GAVIRIA={"autor":"Gaviria Reyes, M.A.; Agusto, M.R.; Trinelli, M.A.; Caselli, A.T.; Dos Santos Afonso, M.; Calabrese, S.","anio":2016,"titulo":"Estudio hidrogeoquímico de las áreas termales del Complejo Volcánico Copahue-Caviahue (Rev. Asoc. Geol. Argentina 73(2):256-269)","tipo":"FQ","link":U_GAVIRIA}
MDPI={"autor":"(autores no extraídos; artículo Microorganisms 3(3):344)","anio":2015,"titulo":"Copahue geothermal system (descripción y microbiología de Las Máquinas / Las Maquinitas)","tipo":"B","link":U_MDPI}
ALPEHUE={"autor":"Muñoz-Sáez, C.; Pérez-Núñez, C.; Martini, S.; Vargas-Barrera, A.; Reich, M.; Morata, D.; Manga, M.","anio":2020,"titulo":"The Alpehue geyser field, Sollipulli Volcano, Chile (J. Volcanol. Geotherm. Res. 406:107065)","tipo":"G","link":U_ALPEHUE}
T_BERRIOS={"autor":"Berríos Guerra, C.A.","anio":2015,"titulo":"Caracterización geoquímica de sistemas geotermales en zonas de transición: volcanes Nevados de Chillán y Copahue (Memoria Geóloga)","universidad":"Universidad de Chile","link":U_BERRIOS}
T_CELIS={"autor":"Celis Abarzúa, R.A.","anio":2012,"titulo":"Caracterización geoquímica del sistema geotermal Termas de Puyehue-Aguas Calientes, Región de los Lagos, Chile (Memoria Geólogo)","universidad":"Universidad de Chile","link":U_CELIS}
T_ALLENDE={"autor":"Allende Carreño, K.F.","anio":2017,"titulo":"Procesos hidrogeoquímicos en aguas termales del fiordo Puyuhuapi, XI Región de Aysén (Memoria Geóloga)","universidad":"Universidad de Chile","link":U_ALLENDE}
T_NEGRI={"autor":"Negri Soto, A.S.","anio":2017,"titulo":"Origen de los fluidos termales e implicancias para los sistemas geotermales de Aysén: una aproximación desde la hidrogeoquímica (Tesis Magíster)","universidad":"Universidad de Chile","link":U_NEGRIT}
T_PEREZ={"autor":"Pérez Núñez, C.A.S.","anio":2019,"titulo":"Estudio del ambiente de formación de sínteres silíceos en los géiseres de Alpehue, volcán Sollipulli, Sur de Chile (Memoria Geóloga)","universidad":"Universidad de Chile","link":U_PEREZ}
T_FELIU={"autor":"Feliú R., D.","anio":2013,"titulo":"Termas de Skyring: aguas termales en Seno Skyring, desarrollo turístico para Río Verde, Región de Magallanes (Memoria Arquitectura)","universidad":"Universidad de Chile","link":U_FELIU}

rows=[]
def add(nombre, **kw):
    r={f:("NA") for f in FIELDS}
    for f in LIST_FIELDS: r[f]=[]
    r["nombre"]=nombre; r["id"]=slug(kw.pop("id",nombre))
    r.update(kw)
    # counts
    if r["n_estudios_FQ"]=="NA": r["n_estudios_FQ"]=sum(1 for e in r["estudios"] if e.get("tipo")=="FQ")
    if r["n_estudios_G"]=="NA": r["n_estudios_G"]=sum(1 for e in r["estudios"] if e.get("tipo")=="G")
    if r["n_estudios_B"]=="NA": r["n_estudios_B"]=sum(1 for e in r["estudios"] if e.get("tipo")=="B")
    if r["n_estudios_Pel"]=="NA": r["n_estudios_Pel"]=sum(1 for e in r["estudios"] if e.get("tipo")=="Pel")
    if r["n_estudios_T"]=="NA": r["n_estudios_T"]=sum(1 for e in r["estudios"] if e.get("tipo")=="T")
    rows.append(r)

def tec(path): return U_TEC+path
LOFZ="falla Liquiñe-Ofqui"

# ================= ÑUBLE =================
add("Termas de Chillán", alias=["Nevados de Chillán","Termas Minerales de Chillán","Aguas Calientes (Chillán)","Roca Verde","Casa Roja","Olla del Mote","Valle Hermoso"],
 region="Ñuble", comuna="Pinto", lat=-36.909133, lon=-71.418509, precision_coord="aprox", fuente_coord=tec("termas-de-chillan-35"),
 tipo_manifestacion="manantial; fumarola; baño de barro", origen_geologico="volcánico (Complejo Volcánico Nevados de Chillán)",
 T_medida_C="Roca Verde 68 (M); Casa Roja 82 (M); Olla del Mote 91 (M); fumarolas hasta ~125 (M)", T_fuente_medida="Wrage et al. 2017 (muestras RV, CR, OM); Berríos 2015 (fumarolas)",
 T_declarada_C="NA", pH="RV 3.9; CR 2.6; OM 2.4 (M, Wrage 2017); aguas ácidas a neutras 3-7 (Berríos 2015)", tipo_quimico="ácido-SO4 (RV, CR, OM; Wrage 2017)",
 iones_resumen="Sulfuros de sodio altos, azufre y hierro (Rodríguez 1935 citado en Wikipedia); geotermómetro sílice 150-200 °C, gases 120-150 °C (Berríos 2015)", isotopos="δD/δ18O recarga meteórica (Berríos 2015)",
 estudios=[WRAGE,{"autor":"Orozco, G.; Jara, G.; Bertin, D.","anio":2016,"titulo":"Peligros del Complejo Volcánico Nevados de Chillán (SERNAGEOMIN)","tipo":"Pel","link":"https://www.sernageomin.cl/wp-content/uploads/volcanes/01/M396_Peligros_Nevados_de_Chillan.pdf"},{"autor":"Rodríguez R., E.","anio":1935,"titulo":"Breves apuntes sobre las Termas de Chillán","tipo":"FQ","link":"https://obtienearchivo.bcn.cl/obtienearchivo?id=documentos/10221.1/53530/1/202885.pdf"}],
 tesis=[T_BERRIOS], infraestructura=["hotel","cabañas","spa","piscinas","restaurante"], categoria="lujo", estado="operativa",
 operador="Sociedad Turismo y Gestión Hotelera Ñuble Ltda. (concesión Municipalidad de Chillán hasta 2038); marca Nevados de Chillán", administracion_comunitaria=False, web="https://www.nevadosdechillan.com/",
 redes_sociales=[{"plataforma":"Instagram","url":"https://instagram.com/nevadosdechillan","seguidores_aprox":"NA"},{"plataforma":"Facebook","url":"https://facebook.com/nevadosdechillan","seguidores_aprox":"NA"},{"plataforma":"YouTube","url":"https://youtube.com/channel/UCai0b2vM5thJK3Gt74rUupQ","seguidores_aprox":"NA"},{"plataforma":"TikTok","url":"https://tiktok.com/@nevadosdechillan","seguidores_aprox":"NA"}],
 barros="declarado", barro_detalle="Baños de vapor naturales y de barro (Diario Concepción 2019); 4 piscinas de aguas sulfatadas y con fierro",
 propiedades_declaradas=["reumatismo","dispepsia","acné rosácea","pénfigo","psoriasis","reconocidas curativas por MINSAL 1954 (Wikipedia)"],
 indicaciones_historicas="Mencionadas por Diego de Rosales 1703; primeras construcciones 1830; estudio Philippi 1862; estudio médico Rodríguez 1935; MINSAL 1954",
 pueblo_originario="Mapuche (pueblos originarios atribuían poderes curativos, Wikipedia)", toponimia="NA", uso_ancestral="declarado (Wikipedia es)",
 area_protegida="Colindante Reserva Nacional Ñuble (baños termales en Valle Hermoso según Sernatur 2012)", seguridad="Pozas ácidas y a ebullición (Olla del Mote 91 °C, pH 2.4); zona de peligro volcánico (SERNAGEOMIN)",
 noticias=[{"medio":"Emol","anio":2017,"titulo":"Termas de Chillán: una zona que invita a disfrutar de la naturaleza","link":"https://www.emol.com/noticias/Tendencias/2017/03/07/848258/Termas-de-Chillan-una-zona-que-invita-a-disfrutar-de-la-naturaleza.html"}],
 fuentes=["https://es.wikipedia.org/wiki/Termas_de_Chill%C3%A1n",U_WRAGE,U_BERRIOS,"https://www.nevadosdechillan.com/",tec("termas-de-chillan-35"),U_DIARIOC],
 notas="Ficha agrupa las manifestaciones del sector Termas/Valle Hermoso/Aguas Calientes del CVNCh. Alto Nevados sufrió incendio el 6-9-2026 (web operador). Berríos 2015 nombra además Baños del Rafa, Baños San Lorenzo y Baños de Cato en el complejo.")

add("Termas Valle Hermoso", alias=["Valle Hermoso Nevados de Chillán"], region="Ñuble", comuna="Pinto", lat=-36.9039832, lon=-71.9685417, precision_coord="aprox", fuente_coord=tec("termas-valle-hermoso-114")+" (coordenada dudosa: cae lejos del valle)",
 tipo_manifestacion="pozón", origen_geologico="volcánico (Nevados de Chillán)", infraestructura=["piscinas","spa","camping","cabañas","restaurante"], categoria="medio", estado="operativa",
 operador="Nevados de Chillán", administracion_comunitaria=False, web="https://www.nevadosdechillan.com/", pueblo_originario="Mapuche",
 fuentes=[tec("termas-valle-hermoso-114"),"https://www.nevadosdechillan.com/"], notas="Centro de piscinas termales y 36 departamentos del mismo complejo Nevados de Chillán; usa agua del mismo sistema. Sin datos medidos propios.")

add("Aguas Calientes (Nevados de Chillán)", alias=["Termas Aguas Calientes Chillán"], region="Ñuble", comuna="Pinto", tipo_manifestacion="manantial; pozón natural", origen_geologico="volcánico (Nevados de Chillán)",
 T_declarada_C="'agradable' (sin valor)", T_fuente_declarada="Meteored 2026", infraestructura=["ninguna"], categoria="natural", estado="operativa", administracion_comunitaria="NA",
 precio_declarado="gratis", pueblo_originario="Mapuche", seguridad="Sendero ~10 km ida y vuelta de alta dificultad; nieve en invierno",
 fuentes=["https://www.meteored.cl/noticias/ocio/termas-gratuitas-en-chile-bienestar-natural-sin-gastar-un-peso-entre-vapor-y-paisajes-salvajes.html",U_BERRIOS], notas="Sector de emanaciones de agua caliente y fumarolas del CVNCh (Berríos 2015). Sin coordenadas en fuentes consultadas.")

# ================= BIOBÍO =================
add("Termas de Nitrao", alias=["Nitrao"], region="Biobío", comuna="Alto Biobío", lat=-37.692529, lon=-71.294956, precision_coord="aprox", fuente_coord=tec("termas-de-nitrao-102"),
 tipo_manifestacion="manantial", origen_geologico="NA", infraestructura=["tinajas","cabañas","camping"], categoria="rústico", estado="operativa",
 operador="Pehuenches residentes del sector (comunidad Malla-Malla)", administracion_comunitaria=True, precio_declarado="'precio reducido' (sin monto)",
 pueblo_originario="Pehuenche", region_cultural="Pewenmapu (Alto Biobío)", uso_ancestral="atendidas por comunidad pehuenche (Sernatur 2012; SIT Rural 2019)",
 fuentes=[U_SERN_VIII,U_SITRURAL_AB,tec("termas-de-nitrao-102"),U_DIARIOC], notas="Sernatur 2012: estado de conservación 'MALA', temporada dic-mar, 9 casetas con tinajas. Ubicadas en límite comunidades Malla-Malla y Trapa-Trapa, río Queuco.")

add("Baños Trapa-Trapa", alias=["Termas de Trapa Trapa","Liray"], region="Biobío", comuna="Alto Biobío", lat=-37.2167, lon=-71.1667, precision_coord="aprox", fuente_coord="Risopatrón 1924 (37°13'S 71°10'W) vía Wikipedia es; probablemente impreciso",
 tipo_manifestacion="manantial", origen_geologico="NA", T_medida_C=45.0, T_fuente_medida="Wrage et al. 2017 (muestra TT)", pH=7.8, tipo_quimico="Na-Cl (Wrage 2017)",
 iones_resumen="sulfatos y fosfatos de soda, cal, magnesia, hierro (Asta-Buruaga 1899 vía Wikipedia)", estudios=[WRAGE], infraestructura=["ninguna"], categoria="natural", estado="desconocido",
 administracion_comunitaria="NA", pueblo_originario="Pehuenche (comunidad Trapa Trapa)", region_cultural="Pewenmapu", toponimia="reduplicación de 'thapum' = torcer (Asta-Buruaga 1899)", toponimia_fuente="https://es.wikipedia.org/wiki/Ba%C3%B1os_Trapa-Trapa",
 indicaciones_historicas="Aguas reconocidas en 1858; uso medicinal (Wikipedia)", fuentes=["https://es.wikipedia.org/wiki/Ba%C3%B1os_Trapa-Trapa",U_WRAGE,U_SITRURAL_AB], notas="SIT Rural 2019 las nombra junto a Nitrao y 'Los Copahues' como baños a orillas del Queuco.")

add("Termas Kokiyen", alias=["Chichintahue","Chichintawue","Termas Kokiyen Chichintawue"], region="Biobío", comuna="Alto Biobío", lat=-37.6814375, lon=-71.4341875, precision_coord="aprox", fuente_coord=tec("termas-kokiyen-chichintawue-110"),
 tipo_manifestacion="manantial", infraestructura=["ninguna"], categoria="natural", estado="desconocido", pueblo_originario="Pehuenche (comunidad Cauñicu)", region_cultural="Pewenmapu",
 fuentes=[tec("termas-kokiyen-chichintawue-110")], notas="Valle del Queuco, acceso 4x4 y sendero 300 m al estero Kokiyen.")

add("Termas del Avellano", alias=["El Avellano"], region="Biobío", comuna="Alto Biobío", lat=-37.990254, lon=-71.529982, precision_coord="aprox", fuente_coord=tec("termas-del-avellano-2"),
 altitud_m="3164 (SIT Rural 2019; valor dudoso)", tipo_manifestacion="pozón", T_medida_C=78.0, T_fuente_medida="Wrage et al. 2017 (muestra AV)", pH=7.7, tipo_quimico="Na-Cl (Wrage 2017)",
 T_declarada_C="~40", T_fuente_declarada="Diario Concepción 2019", estudios=[WRAGE], infraestructura=["pozones","camping"], categoria="rústico", estado="operativa",
 operador="Comunidad pehuenche Quepuca Ralco (SIT Rural 2019)", administracion_comunitaria=True, precio_declarado="camping bajo costo", pueblo_originario="Pehuenche", region_cultural="Pewenmapu",
 fuentes=[tec("termas-del-avellano-2"),U_SITRURAL_AB,U_DIARIOC,U_WRAGE,U_MUNI_AB], notas="Ribera del río Biobío; en primavera el río inunda los pozones. Contacto muni: +56 9 4762 8633.")

add("Termas de Chancho Co", alias=["Chanchokó","Chancho-Có","Termas de Chanchoko"], region="Biobío", comuna="Alto Biobío", lat=-37.818919, lon=-71.163611, precision_coord="aprox", fuente_coord="coordenada entregada por el solicitante",
 tipo_manifestacion="baño de barro; fumarola", origen_geologico="volcánico (Copahue, flanco norte)", T_medida_C="89.8 (2012); 82.9 (2013)", T_fuente_medida="Gaviria et al. 2016 (pozo de barro)", pH="3.37; 3.62",
 tipo_quimico="ácido-SO4", iones_resumen="SO4 2079-2165; Cl 4-22; Fe 81-654; Si 451-483; Al 300 ppm (Gaviria 2016; tabla con posible desalineación)", estudios=[GAVIRIA,MDPI],
 infraestructura=["ninguna"], categoria="natural", estado="operativa", administracion_comunitaria="NA", pueblo_originario="Pehuenche (sector Trapa Trapa)", region_cultural="Pewenmapu",
 seguridad="Pozas a 83-90 °C y pH ~3.4; fumarolas; acceso 4x4", fuentes=[U_GAVIRIA,U_MDPI,U_MUNI_AB], notas="Depósitos de azufre, alunita, jarosita. Contacto muni Alto Biobío +56 9 7526 7483.")

add("Copahue chileno", alias=["Pucón-Mahuida","Pucón Mahuida","Los Copahues"], region="Biobío", comuna="Alto Biobío", origen_geologico="volcánico (Copahue)", tipo_manifestacion="manantial; fumarola",
 T_medida_C="Pucón Mahuida 47 (M, Wrage 2017); 45 (Berríos 2015)", T_fuente_medida="Wrage et al. 2017 (PM); Berríos 2015", pH="7.9 (PM)", tipo_quimico="HCO3 (PM, Wrage 2017)",
 iones_resumen="Geotermómetros gaseosos Copahue 200-250 °C (Berríos 2015)", estudios=[WRAGE,GAVIRIA,MDPI], tesis=[T_BERRIOS], infraestructura=["ninguna"], categoria="natural", estado="desconocido",
 pueblo_originario="Pehuenche", region_cultural="Pewenmapu", fuentes=[U_WRAGE,U_BERRIOS,U_GAVIRIA,U_MDPI,U_SITRURAL_AB],
 notas="ADVERTENCIA: Anfiteatro, Las Máquinas y Las Maquinitas están en territorio argentino (Caviahue) según Gaviria 2016; Wrage 2017 los muestreó (AF 87 °C pH 2.7; LMM 93 °C pH 3.6; LM 88 °C pH 2.2, ácido-SO4). Las Máquinas 36 °C pH 3.2 CE 663 µS/cm; Maquinitas 87 °C pH 2.0 CE 4520 µS/cm, dominadas por Thiomonas/Sulfolobus (Microorganisms 2015). Pucón Mahuida es domo riolítico en flanco SE (Berríos 2015). Sin coordenadas.")

add("Termas de San Lorenzo de Villucura", region="Biobío", comuna="Santa Bárbara", estado="desconocido", categoria="rústico", infraestructura=["ninguna"], administracion_comunitaria="NA",
 fuentes=[U_DIARIOC], notas="Mencionadas en Diario Concepción 2019 como muy concurridas y cuidadas por residentes. Sin más datos. No confundir con Baños San Lorenzo del CVNCh.")

# ================= ARAUCANÍA =================
add("Termas de Pemehue", alias=["Pemehue"], region="La Araucanía", comuna="Collipulli", lat=-38.069608, lon=-71.703425, precision_coord="aprox", fuente_coord=tec("termas-pemehue-10"), altitud_m=700,
 tipo_manifestacion="manantial", T_medida_C=38.5, T_fuente_medida="Wrage et al. 2017 (PE)", pH=7.5, tipo_quimico="Na-Cl (Wrage 2017)", T_declarada_C="27-37", T_fuente_declarada="termasenchile.cl",
 estudios=[WRAGE], infraestructura=["piscinas","pozones","tinajas","camping","restaurante"], categoria="rústico", estado="operativa", administracion_comunitaria="NA",
 propiedades_declaradas=["aguas alcalinas ricas en sales y minerales"], pueblo_originario="Mapuche", area_protegida="Reserva Nacional Malleco (localidad según Sernatur 2012)",
 fuentes=[U_SERN_IX,tec("termas-pemehue-10"),U_WRAGE], notas="Ribera sur del río Renaico, cordillera de Pemehue. Sernatur 2012: propiedad pública/pública, sin servicios, temporada todo el año.")

add("Termas de Pelehue", alias=["Pelehue"], region="La Araucanía", comuna="Lonquimay", tipo_manifestacion="manantial", origen_geologico="volcánico", T_medida_C=82.0, T_fuente_medida="Wrage et al. 2017 (PL)", pH=3.3, tipo_quimico="ácido-SO4 (Wrage 2017)",
 estudios=[WRAGE], infraestructura=["ninguna"], categoria="natural", estado="desconocido", pueblo_originario="Pehuenche/Mapuche", seguridad="Agua ácida a 82 °C", fuentes=[U_WRAGE], notas="Sin coordenadas ni comuna verificada (asignada Lonquimay por aproximación).")

add("Baños de Coyuco", alias=["Termas de Coyuco"], region="La Araucanía", comuna="Lonquimay", tipo_manifestacion="pozón", T_medida_C=36.0, T_fuente_medida="Wrage et al. 2017 (CU)", pH=6.2, tipo_quimico="HCO3 (Wrage 2017)",
 estudios=[WRAGE], infraestructura=["pozones"], categoria="natural", estado="operativa", precio_declarado="gratis", administracion_comunitaria="NA", pueblo_originario="Pehuenche/Mapuche",
 fuentes=[U_WRAGE,U_METEO_MAL], notas="Valle del río Pulul, entre araucarias y coihues; dos pocitos naturales techados en madera (Meteored). Comuna aproximada.")

add("Termas Malleco", alias=["Termas de Tolhuaca","Tolhuaca"], region="La Araucanía", comuna="Curacautín", lat=-38.23463, lon=-71.72834, precision_coord="exacta", fuente_coord="termasmalleco.cl",
 tipo_manifestacion="manantial; géiser (gruta)", origen_geologico="volcánico (Tolhuaca)", T_medida_C="85.5 (Malleco); 92 (Tolhuaca Vn., JM)", T_fuente_medida="Wrage et al. 2017 (MA, JM)", pH="8.4 (MA); 2.4 (JM)",
 tipo_quimico="Na-Cl (MA); ácido-SO4 (JM) (Wrage 2017)", T_declarada_C="86 (surgencia)", T_fuente_declarada="Meteored", estudios=[WRAGE],
 infraestructura=["hotel","spa","piscinas","restaurante","camping"], categoria="medio", estado="operativa", operador="Turismo Patagonia Andina Ltda.", administracion_comunitaria=False, web="https://www.termasmalleco.cl/",
 redes_sociales=[{"plataforma":"Instagram","url":"https://instagram.com/termasmalleco","seguidores_aprox":"NA"},{"plataforma":"Facebook","url":"https://facebook.com/TermasMalleco","seguidores_aprox":"NA"}],
 precio_declarado="Baja $28.000 adulto/$18.000 niño; alta $32.000/$22.000 (Meteored)", propiedades_declaradas=["alta concentración de minerales"], indicaciones_historicas="Reabiertas en enero de 2009 tras remodelación (Sernatur 2012); 100 camas",
 pueblo_originario="Mapuche", area_protegida="Colindante Parque Nacional Tolhuaca", seguridad="Surgencia 86 °C en gruta de géiseres", fuentes=["https://www.termasmalleco.cl/",U_SERN_IX,U_WRAGE,U_METEO_MAL])

add("Malalcahuello Thermal Resort & Spa", alias=["Termas de Malalcahuello"], region="La Araucanía", comuna="Curacautín", lat=-38.49007, lon=-71.58489, precision_coord="aprox", fuente_coord="UTM 19S 274555E/5736642N Muñoz et al. 2011 (pozos), convertida", altitud_m=970,
 tipo_manifestacion="pozo", origen_geologico="volcánico (Sierra Nevada / valle Cautín)", T_medida_C="44 (pozo 25 m); 43 (pozo 80 m)", T_fuente_medida="Muñoz et al. 2011 (ML1, ML2)", pH="9.4; 9.5",
 tipo_quimico="Na-SO4(-HCO3) alcalina (Muñoz 2011)", iones_resumen="ML1: Na 40, K 1.6, Ca 4.2, Cl 15, SO4 47, HCO3 33, SiO2 47, B 1.0 mg/L; TDS 130-210", isotopos="δD -68, δ18O -9.9/-10 ‰ (Muñoz 2011)",
 T_declarada_C="36-40 (piscinas)", T_fuente_declarada="Meteored", estudios=[MUNOZ], infraestructura=["hotel","cabañas","spa","piscinas","restaurante"], categoria="lujo", estado="operativa", administracion_comunitaria=False, web="https://www.malalcahuello.cl/",
 precio_declarado="$29.990 piscina techada 3 h (Meteored)", pueblo_originario="Mapuche-Pehuenche", fuentes=[U_MUNOZ,U_METEO_MAL,tec("malalcahuello-thermal-resort-spa-6")], notas="Agua de pozos (25, 80 y 120 m). Coordenada de termasenchile.cl errónea (apunta a Pucón). Web operador bloqueada a robots.")

add("Termas de Manzanar", alias=["Manzanar"], region="La Araucanía", comuna="Curacautín", lat=-38.46563, lon=-71.70808, precision_coord="aprox", fuente_coord="UTM 19S 263729E/5739046N Muñoz et al. 2011, convertida", altitud_m=745,
 tipo_manifestacion="pozo", origen_geologico="volcánico (Sierra Nevada / valle Cautín)", T_medida_C="52 (pozo 4 m); 48 (pozo 120 m)", T_fuente_medida="Muñoz et al. 2011 (MR1, MR2)", pH="9.7",
 tipo_quimico="Na-SO4(-HCO3) alcalina", iones_resumen="MR1: Na 69, K 2, Ca 1.4, Cl 19, SO4 50, HCO3 38, SiO2 59, B 0.6 mg/L; geotermómetros 60-82 °C", isotopos="δD -63/-64, δ18O -9.7 ‰",
 estudios=[MUNOZ], infraestructura=["hotel","piscinas","tinajas","spa","restaurante"], categoria="medio", estado="operativa", operador="Turismo Patagonia Andina (pase anual conjunto con Malleco/Menetúe/Coñaripe)", administracion_comunitaria=False, web="https://www.termasdemanzanar.cl/",
 precio_declarado="Baja $25.000/$15.000; alta $28.000/$18.000 (Meteored)", indicaciones_historicas="Hotel inaugurado en 1952 (Sernatur 2012)", pueblo_originario="Mapuche-Pehuenche", fuentes=[U_MUNOZ,U_SERN_IX,U_METEO_MAL])

add("Baños del Toro (Sierra Nevada)", alias=["Sierra Nevada","Termas Sierra Nevada"], region="La Araucanía", comuna="Curacautín", lat=-38.57478, lon=-71.61585, precision_coord="aprox", fuente_coord="UTM 19S 272122E/5727164N Muñoz et al. 2011, convertida", altitud_m=1341,
 tipo_manifestacion="fumarola; pozón ácido", origen_geologico="volcánico (Sierra Nevada)", T_medida_C="89-90 (Muñoz 2011); 87 (Wrage 2017 BT)", T_fuente_medida="Muñoz et al. 2011; Wrage et al. 2017", pH="2.1 (Muñoz); 3.4 (Wrage)",
 tipo_quimico="ácido-SO4 (Ca-Mg-SO4)", iones_resumen="SO4 3796, Ca 211, Mg 82, Fe 131, Al 322, SiO2 323 mg/L; TDS ~3000; gas: CO2 727, H2S 55 mmol/mol; geotermómetro gas 216 °C", isotopos="δD -75, δ18O -10 ‰",
 estudios=[MUNOZ,WRAGE], infraestructura=["ninguna"], categoria="natural", estado="desconocido", pueblo_originario="Mapuche-Pehuenche", seguridad="Pozas ácidas (pH 2) a ~90 °C; fumarolas", fuentes=[U_MUNOZ,U_WRAGE])

add("Aguas de la Vaca", alias=["Agua de la Vaca"], region="La Araucanía", comuna="Curacautín", lat=-38.57923, lon=-71.62755, precision_coord="aprox", fuente_coord="UTM 19S 271116E/5726641N Muñoz et al. 2011, convertida", altitud_m=1070,
 tipo_manifestacion="manantial (burbujeante)", origen_geologico="volcánico (Sierra Nevada)", T_medida_C="57-60 (Muñoz 2011); 35 (Wrage 2017 VA)", T_fuente_medida="Muñoz et al. 2011; Wrage et al. 2017", pH="7.0 (Muñoz); 7.2 (Wrage)",
 tipo_quimico="Na-Cl-SO4 neutra", iones_resumen="Na 167, K 29, Ca 95, Cl 332, SO4 174, HCO3 58, SiO2 125, B 18, Li 2.1 mg/L; TDS 950", isotopos="δD -68, δ18O -9.5 ‰",
 estudios=[MUNOZ,WRAGE], infraestructura=["ninguna"], categoria="natural", estado="desconocido", pueblo_originario="Mapuche-Pehuenche", fuentes=[U_MUNOZ,U_WRAGE], notas="Cañón del Blanco ofrece 'fudres y cajones de la vaca' y 'barros del toro', posiblemente asociados a estas fuentes.")

add("Termas Cañón del Blanco", region="La Araucanía", comuna="Curacautín", lat=-38.5447673, lon=-72.2410143, precision_coord="aprox", fuente_coord=tec("termas-canon-del-blanco-112")+" (coordenada dudosa; cae en Curacautín urbano)",
 tipo_manifestacion="manantial", infraestructura=["pozones","tinajas","camping","cabañas"], categoria="rústico", estado="operativa", administracion_comunitaria="NA", barros="declarado", barro_detalle="'barros del toro'",
 pueblo_originario="Mapuche-Pehuenche", fuentes=[tec("termas-canon-del-blanco-112")], notas="Hostal, glamping, cabalgatas, tubing.")

add("Termas de Río Blanco (Curacautín)", alias=["Río Blanco"], region="La Araucanía", comuna="Curacautín", tipo_manifestacion="manantial", T_medida_C=51.0, T_fuente_medida="Wrage et al. 2017 (RB)", pH=7.7, tipo_quimico="Na-Cl (Wrage 2017)",
 estudios=[WRAGE], categoria="NA", estado="desconocido", pueblo_originario="Mapuche-Pehuenche", fuentes=[U_WRAGE], notas="Wrage 2017 'Termas de Río Blanco' sin coordenadas publicadas en la copia consultada; ubicación en el valle del río Blanco (Curacautín) asumida. Muñoz 2011 muestreó el río Blanco (17 °C, no termal).")

add("Termas de Balboa", region="La Araucanía", comuna="Curacautín", tipo_manifestacion="manantial", T_medida_C=45.0, T_fuente_medida="Wrage et al. 2017 (BB)", pH=7.3, tipo_quimico="Na-Cl (Wrage 2017)", estudios=[WRAGE], estado="desconocido", pueblo_originario="Mapuche-Pehuenche",
 fuentes=[U_WRAGE], notas="Solo datos de Wrage 2017; sin coordenadas ni información turística encontrada; comuna aproximada.")

add("Termas de Alpehue", alias=["Termas de Queipue","Alpehue","Géiseres de Alpehue"], region="La Araucanía", comuna="Melipeuco", lat=-38.852339, lon=-71.693132, precision_coord="aprox", fuente_coord=tec("termas-de-queipue-o-alpehue-80"),
 tipo_manifestacion="géiser; manantial; baño de barro", origen_geologico="volcánico (Sollipulli)", T_medida_C=">90 (ebullición)", T_fuente_medida="Pérez 2019; Muñoz-Sáez et al. 2020", pH="7-8", tipo_quimico="Na-Cl alcalino, alta sílice",
 iones_resumen="SiO2 369-412 mg/L; reservorio ~200 °C; sínter opal-A, edad hasta 7.37 ka", isotopos="δD/δ18O origen meteórico (Muñoz-Sáez 2020)", estudios=[ALPEHUE], tesis=[T_PEREZ],
 infraestructura=["ninguna"], categoria="natural", estado="operativa", pueblo_originario="Mapuche", seguridad="Géiseres y pozas en ebullición en cañón profundo; acceso por canyoning", fuentes=[U_ALPEHUE,U_PEREZ,tec("termas-de-queipue-o-alpehue-80")],
 notas="Al menos 4 géiseres y 11 rasgos termales en ~0.2 km2.")

add("Termas de Molulco", region="La Araucanía", comuna="Melipeuco", tipo_manifestacion="manantial", origen_geologico="volcánico (Sollipulli)", T_declarada_C="35-45", T_fuente_declarada="termasenchile.cl",
 infraestructura=["pozones","restaurante"], categoria="rústico", estado="operativa", pueblo_originario="Mapuche", fuentes=[tec("termas-de-molulco-78")], notas="Junto al río Pichapinga, 26 km de Melipeuco. Coordenada de termasenchile.cl inválida (idéntica a Trancura), omitida.")

add("Termas Huife", alias=["Hotel y Termas Huife"], region="La Araucanía", comuna="Pucón", lat=-39.227893, lon=-71.657372, precision_coord="aprox", fuente_coord=tec("hotel-y-termas-huife-3")+"; termashuife.cl (-39.228,-71.660)",
 tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="35-40 (piscinas)", T_fuente_declarada="termashuife.cl; chile.travel", infraestructura=["hotel","spa","piscinas","restaurante"], categoria="lujo", estado="operativa",
 administracion_comunitaria=False, web="https://www.termashuife.cl/", redes_sociales=[{"plataforma":"Facebook","url":"https://facebook.com/HotelyTermasHuife","seguidores_aprox":"NA"},{"plataforma":"Instagram","url":"https://instagram.com/hotelytermashuife","seguidores_aprox":"NA"}],
 precio_declarado="Día completo $40.000 adulto; $25.000 niño; $32.000 adulto mayor (web); $35.000/$20.000 (Meteored)", pueblo_originario="Mapuche", fuentes=["https://www.termashuife.cl/",tec("hotel-y-termas-huife-3"),U_CT_PUCON,U_METEO_PUC], notas="Ribera río Liucura, 33 km de Pucón; 300 ha.")

add("Termas Los Pozones", region="La Araucanía", comuna="Pucón", lat=-39.225959, lon=-71.645008, precision_coord="aprox", fuente_coord=tec("termas-los-pozones-5"), tipo_manifestacion="pozón", origen_geologico=LOFZ,
 T_declarada_C="20-40", T_fuente_declarada="chile.travel", infraestructura=["pozones","camping"], categoria="rústico", estado="operativa", pueblo_originario="Mapuche", fuentes=[tec("termas-los-pozones-5"),U_CT_PUCON], notas="5-6 pozones en roca junto al río Liucura, sector Huife.")

add("Termas Quimey-Co", alias=["Quimeyco"], region="La Araucanía", comuna="Pucón", lat=-39.218964, lon=-71.696425, precision_coord="aprox", fuente_coord=tec("termas-quimeyco-13"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C=45.0, T_fuente_medida="Wrage et al. 2017 (QC)", pH=8.1, tipo_quimico="Na-Cl (Wrage 2017)", T_declarada_C="36-43 (piscinas)", T_fuente_declarada="chile.travel; termasenchile.cl", estudios=[WRAGE],
 infraestructura=["piscinas","spa","restaurante"], categoria="medio", estado="operativa", precio_declarado="$35.000 adulto; $30.000 niño/adulto mayor (Meteored)", propiedades_declaradas=["rica en sales y minerales","declarada 'Fuente Curativa' en 2014 (chile.travel)"],
 pueblo_originario="Mapuche", fuentes=[tec("termas-quimeyco-13"),U_WRAGE,U_CT_PUCON,U_CT_2026,U_METEO_PUC])

add("Termas Menetúe", alias=["Parque Termal Menetúe"], region="La Araucanía", comuna="Pucón", lat=-39.330803, lon=-71.719459, precision_coord="aprox", fuente_coord=tec("termas-menetue-7")+"; menetueparquetermal.cl (-39.3300,-71.7212)",
 tipo_manifestacion="manantial", origen_geologico=LOFZ, T_medida_C=42.0, T_fuente_medida="Wrage et al. 2017 (ME)", pH=9.2, tipo_quimico="Na-Cl (Wrage 2017)", T_declarada_C="37-39 (reseñas)", T_fuente_declarada="menetueparquetermal.cl (reseñas)",
 estudios=[WRAGE], infraestructura=["cabañas","spa","piscinas","restaurante"], categoria="lujo", estado="operativa", operador="Menetue Inmobiliaria / Grupo Patagonia Andina", administracion_comunitaria=False, web="https://www.menetueparquetermal.cl/",
 redes_sociales=[{"plataforma":"Instagram","url":"https://instagram.com/termasmenetue","seguidores_aprox":"NA"},{"plataforma":"Facebook","url":"https://facebook.com/termasmenetue","seguidores_aprox":"NA"}],
 precio_declarado="Baja $28.000 adulto; $20.000 niño (Meteored)", pueblo_originario="Mapuche", fuentes=[tec("termas-menetue-7"),"https://www.menetueparquetermal.cl/",U_WRAGE,U_METEO_PUC], notas="40 ha junto a laguna Ancapulli; 'primer viñedo termal'.")

add("Termas de Palguín", alias=["Palguín"], region="La Araucanía", comuna="Pucón", tipo_manifestacion="manantial", origen_geologico=LOFZ, T_medida_C="50 (Wrage 2017); 35-36 (Alam 2010)", T_fuente_medida="Wrage et al. 2017 (PA); Alam et al. 2010", pH="8.9 (Wrage); 8.7 (Alam)",
 tipo_quimico="Na-Cl (Wrage); Na-SO4-HCO3 (Alam)", iones_resumen="Alam 2010: Na 42-53, Ca 4.2, Cl 10-12, SO4 32-38, HCO3 67-81, SiO2 47-52 mg/L; TDS 110", estudios=[WRAGE,ALAM], estado="desconocido", pueblo_originario="Mapuche",
 fuentes=[U_WRAGE,U_ALAM], notas="Sin coordenadas ni información turística actualizada en fuentes consultadas.")

add("Termas San Luis", region="La Araucanía", comuna="Pucón", lat=-39.340013, lon=-71.690846, precision_coord="aprox", fuente_coord=tec("termas-san-luis-15"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="40 (Wrage 2017); 39 (Alam 2010)", T_fuente_medida="Wrage et al. 2017 (SL); Alam et al. 2010", pH="9.3; 9.4", tipo_quimico="Na-Cl (Wrage); Na-SO4 (Alam)", iones_resumen="Alam 2010: Na 55, Ca 5.2, Cl 8, SO4 77, HCO3 29, CO3 12, SiO2 49 mg/L; TDS 170",
 T_declarada_C="36-40 (4 piscinas)", T_fuente_declarada="chile.travel", estudios=[WRAGE,ALAM,SANCHEZ], infraestructura=["hotel","cabañas","piscinas","tinajas","spa","restaurante"], categoria="medio", estado="operativa", propiedades_declaradas=["afecciones de la piel","sistema nervioso","estrés"],
 pueblo_originario="Mapuche", fuentes=[tec("termas-san-luis-15"),U_WRAGE,U_ALAM,U_CT_PUCON], notas="Valle de Curarrehue, ~40 km de Pucón.")

add("Termas de Liucura", region="La Araucanía", comuna="Pucón", lat=-39.256799, lon=-71.821259, precision_coord="aprox", fuente_coord=tec("termas-de-liucura-4"), tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="28-45", T_fuente_declarada="termasenchile.cl",
 infraestructura=["piscinas","pozones","tinajas","camping","cabañas"], categoria="medio", estado="operativa", pueblo_originario="Mapuche", fuentes=[tec("termas-de-liucura-4")])

add("Termas Trancura", alias=["Parque Termal Trancura"], region="La Araucanía", comuna="Curarrehue", tipo_manifestacion="pozo", origen_geologico=LOFZ, T_declarada_C="máx. 42", T_fuente_declarada="termasenchile.cl",
 infraestructura=["piscinas","restaurante"], categoria="medio", estado="operativa", propiedades_declaradas=["certificada 'fuente curativa' por MINSAL (declarado)"], pueblo_originario="Mapuche", fuentes=[tec("termas-trancura-115")],
 notas="1,5 km de Catripulli, 27 km de Pucón; agua de perforaciones. Coordenada de termasenchile.cl inválida, omitida.")

add("Termas Peumayén", alias=["Termas Chile Lodge & Termas Peumayén"], region="La Araucanía", comuna="Pucón", estado="desconocido", pueblo_originario="Mapuche", fuentes=[tec("termas-chile-lodge-termas-peumayen-11")], notas="Ficha de termasenchile.cl no pudo leerse (límite de tasa). Sin datos.")

add("Termas Pucón Indómito", alias=["Pucón Indomito"], region="La Araucanía", comuna="Pucón", lat=-39.2185117, lon=-71.7035593, precision_coord="aprox", fuente_coord=tec("termas-pucon-indomito-107"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_declarada_C="38-40", T_fuente_declarada="Meteored", infraestructura=["piscinas","tinajas","spa","restaurante"], categoria="medio", estado="operativa", precio_declarado="$24.000 adulto; $20.000 niño/adulto mayor (Meteored 2026)", pueblo_originario="Mapuche",
 fuentes=[tec("termas-pucon-indomito-107"),U_METEO_PUC], notas="Camino a Huife, ~30 km de Pucón.")

add("Termas Montevivo", region="La Araucanía", comuna="Pucón", lat=-39.3402502, lon=-71.6933, precision_coord="aprox", fuente_coord=tec("termas-montevivo-123"), tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="39 (piscinas); 20 (fría)", T_fuente_declarada="termasenchile.cl",
 infraestructura=["piscinas","cabañas","spa","restaurante"], categoria="medio", estado="operativa", pueblo_originario="Mapuche", fuentes=[tec("termas-montevivo-123")], notas="Valle de Curarrehue, 27 km de Pucón.")

add("Termas Recuerdo de Ancamil", region="La Araucanía", comuna="Curarrehue", estado="desconocido", pueblo_originario="Mapuche", notas="No se encontró información en las fuentes consultadas (búsqueda sin resultados).")

add("Termas de Panqui", region="La Araucanía", comuna="Curarrehue", lat=-39.215783, lon=-71.488870, precision_coord="aprox", fuente_coord=tec("termas-de-panqui-76"), tipo_manifestacion="pozón", origen_geologico=LOFZ,
 infraestructura=["pozones","camping","hotel","cabañas"], categoria="rústico", estado="operativa", pueblo_originario="Mapuche", fuentes=[tec("termas-de-panqui-76")], notas="4 piscinas al aire libre de distintas temperaturas; camping incluido en entrada.")

add("Termas Angostura", alias=["Termas de Curarrehue","Termas Angostura (ex Curarrehue)"], region="La Araucanía", comuna="Curarrehue", lat=-39.352742, lon=-71.639528, precision_coord="aprox", fuente_coord=tec("termas-angostura-ex-curarrehue-17"),
 tipo_manifestacion="manantial", origen_geologico=LOFZ, infraestructura=["piscinas","restaurante","spa"], categoria="medio", estado="operativa", pueblo_originario="Mapuche", fuentes=[tec("termas-angostura-ex-curarrehue-17")], notas="4 km antes de Curarrehue, solo visitantes de paso.")

add("Parque Termal Botánico", region="La Araucanía", comuna="Pucón", tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="35-41", T_fuente_declarada="chile.travel 2026", infraestructura=["piscinas","spa"], categoria="lujo", estado="operativa",
 precio_declarado="$40.000 adulto; $30.000 niño/adulto mayor, máx. 4 h (Meteored); tour GoChile desde $112.500", propiedades_declaradas=["aguas termales curativas certificadas (declarado)"], pueblo_originario="Mapuche",
 fuentes=[U_CT_2026,U_METEO_PUC,"https://www.gochile.cl/es/tours/excursion_por_el_parque_termal_botanico.htm"], notas="15 km de Pucón, sector Liucura/Caburgua, junto al río Liucura; 10 piscinas (2 en cavernas, 1 en 'palacio de cristal').")

add("Eco Termas Río Blanco (Cunco)", alias=["Termas de Río Blanco Huerquehue","Termas San Sebastián"], region="La Araucanía", comuna="Cunco", lat=-39.108367, lon=-71.613344, precision_coord="aprox", fuente_coord=tec("eco-termas-de-rio-blanco-81"),
 tipo_manifestacion="manantial (al menos 8 vertientes)", origen_geologico=LOFZ, T_declarada_C="48-70", T_fuente_declarada="nomades.com", pH="neutro (declarado, termasenchile.cl)", infraestructura=["pozones"], categoria="natural", estado="operativa",
 operador="San Sebastián y Eco Termas Río Blanco (nomades.com)", pueblo_originario="Mapuche", area_protegida="Parque Nacional Huerquehue (acceso)", fuentes=[tec("eco-termas-de-rio-blanco-81"),U_NOMADES], notas="Caminata ~4 h desde el parque; pozo principal en gruta a 40 m del río Blanco.")

# ================= LOS RÍOS =================
add("Termas Geométricas", region="Los Ríos", comuna="Panguipulli", lat=-39.501990, lon=-71.875070, precision_coord="aprox", fuente_coord=tec("termas-geometricas-22"), tipo_manifestacion="manantial (>60 fuentes)", origen_geologico="volcánico (Villarrica) / "+LOFZ,
 T_medida_C="72 (Alam 2010); 86-89 (estudio previo citado en Sánchez & Alam 2009)", T_fuente_medida="Alam et al. 2010; Sánchez & Alam 2009", pH=8.4, tipo_quimico="Na-SO4 (Alam 2010)", iones_resumen="Na 160, K 9.6, Ca 47, Cl 49, SO4 421, HCO3 29, SiO2 83, B 5.0 mg/L; TDS 540",
 T_declarada_C="80 surgencia; pozones 36-60; uso ~45", T_fuente_declarada="termasgeometricas.cl; Sernatur 2012; termasenchile.cl", estudios=[ALAM,SANCHEZ], infraestructura=["pozones","restaurante"], categoria="lujo", estado="operativa",
 administracion_comunitaria=False, web="https://www.termasgeometricas.cl/", indicaciones_historicas="Diseño del arquitecto Germán del Sol; 17-20 pozones de piedra y pasarelas de madera (450 m)", pueblo_originario="Mapuche",
 area_protegida="Parque Nacional Villarrica (según Sernatur 2012 y termasenchile.cl)", seguridad="Agua a 80 °C en surgencia, enfriada a ~45 °C", fuentes=["https://www.termasgeometricas.cl/",tec("termas-geometricas-22"),U_SERN_XIV,U_ALAM], notas="Web indica 'Próximamente en un nuevo lugar'. Estero Aihué, 16 km de Coñaripe.")

add("Termas de Coñaripe", alias=["Hotel Termas Coñaripe"], region="Los Ríos", comuna="Panguipulli", lat=-39.635648, lon=-71.922947, precision_coord="aprox", fuente_coord=tec("termas-conaripe-18"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="74.6 (Wrage 2017); 55-68 (Alam 2010); 72 (Sánchez & Alam 2009)", T_fuente_medida="Wrage et al. 2017 (CO); Alam et al. 2010; Sánchez & Alam 2009", pH="8.5 (Wrage); 7.9-8.6 (Alam)", tipo_quimico="Na-Cl (Wrage); Na-SO4-HCO3-Cl (Alam)",
 iones_resumen="Alam 2010 (3 muestras): Na 82-136, Cl 50-81, SO4 61-103, HCO3 78-94, SiO2 55-78, B 4.7-7.3 mg/L; TDS 230-350", T_declarada_C=">78 surgencia; piscina 38-40", T_fuente_declarada="El Mostrador 2014",
 estudios=[WRAGE,ALAM,SANCHEZ], infraestructura=["hotel","cabañas","spa","piscinas","restaurante"], categoria="lujo", estado="operativa", operador="Grupo Patagonia Andina (pase anual conjunto); administrador Luis Rojas (2014)", administracion_comunitaria=False,
 barros="declarado", barro_detalle="piscina de barro termal techada", propiedades_declaradas=["rica en litio, sin olor a azufre (El Mostrador 2014)"], pueblo_originario="Mapuche", fuentes=[tec("termas-conaripe-18"),U_SERN_XIV,U_WRAGE,U_ALAM,U_ELMOS_RIOS], notas="Km 15 camino Coñaripe-Liquiñe, lago Pellaifa.")

add("Termas El Rincón", alias=["Termas el Rincon"], region="Los Ríos", comuna="Panguipulli", lat=-39.507271, lon=-71.854600, precision_coord="aprox", fuente_coord=tec("termas-el-rincon-20"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="37 (Wrage 2017); 36 (Alam 2010)", T_fuente_medida="Wrage et al. 2017 (ER); Alam et al. 2010", pH="7.7; 8.0", tipo_quimico="Na-Cl (Wrage); Na-SO4 (Alam)", iones_resumen="Alam: Na 62, Ca 10, Cl 17, SO4 103, HCO3 52, SiO2 69 mg/L; TDS 250",
 estudios=[WRAGE,ALAM], infraestructura=["tinajas","pozones"], categoria="rústico", estado="operativa", web="https://www.termaselrincon.cl/", redes_sociales=[{"plataforma":"Facebook","url":"https://facebook.com/Termas.El.Rincon/","seguidores_aprox":"NA"},{"plataforma":"Instagram","url":"https://instagram.com/termaselrincon/","seguidores_aprox":"NA"}],
 pueblo_originario="Mapuche", seguridad="Web advierte restricciones para embarazadas, hipertensos y cardiópatas", fuentes=["https://www.termaselrincon.cl/",tec("termas-el-rincon-20"),U_WRAGE,U_ALAM], notas="Camino Los Cajones km 19.")

add("Termas Vergara", region="Los Ríos", comuna="Panguipulli", lat=-39.509398, lon=-71.894151, precision_coord="aprox", fuente_coord=tec("termas-vergara-88"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="41 (Alam 2010)", T_fuente_medida="Alam et al. 2010; Sánchez & Alam 2009 (pH 7.9)", pH="7.8-7.9", tipo_quimico="Na-SO4 (Alam 2010)", iones_resumen="Na 72, K 5, Ca 17, Cl 18, SO4 151, HCO3 48, SiO2 68 mg/L; TDS 240", T_declarada_C="38-45", T_fuente_declarada="termasenchile.cl",
 estudios=[ALAM,SANCHEZ], infraestructura=["piscinas","cabañas","restaurante"], categoria="medio", estado="operativa", operador="Cipriano Vergara (contacto 2014)", propiedades_declaradas=["dolores musculares, reumáticos y articulares","antiestrés","desintoxicación"], pueblo_originario="Mapuche",
 fuentes=[tec("termas-vergara-88"),U_SERN_XIV,U_ALAM,U_ELMOS_RIOS], notas="Camino Los Cajones km 14; 6 piscinas, tobogán 20 m, canopy.")

add("Termas Río Liquiñe", alias=["Termas de Liquiñe","Hostería Termas de Liquiñe","Termas Liquiñe"], region="Los Ríos", comuna="Panguipulli", lat=-39.740884, lon=-71.855548, precision_coord="aprox", fuente_coord=tec("termas-rio-liquine-24"), altitud_m="~250 (Liquiñe, Wikipedia)",
 tipo_manifestacion="manantial", origen_geologico=LOFZ, T_medida_C="70-71 (Alam 2010, 4 muestras); 73.3 (Sánchez & Alam 2009)", T_fuente_medida="Alam et al. 2010; Sánchez & Alam 2009", pH="8.8-9.5", tipo_quimico="Na-SO4 (Alam 2010)",
 iones_resumen="Na 26-73, Cl 7-16, SO4 30-81, HCO3 24-67, SiO2 41-87 mg/L; TDS 130-260", T_declarada_C="~80 surgencia; piscina 45", T_fuente_declarada="termasenchile.cl", estudios=[ALAM,SANCHEZ],
 infraestructura=["cabañas","piscinas","restaurante"], categoria="medio", estado="operativa", operador="Termas Río Liquiñe (contacto Víctor García, 2014); Termas de Liquiñe = Bienestar Social Armada de Chile (Sernatur 2012)", administracion_comunitaria=False,
 propiedades_declaradas=["azufre, sílice, litio, sodio, potasio, aluminio, cobre, hierro (declarado)"], pueblo_originario="Mapuche", toponimia="Liquiñe = 'ojos lagrimosos' (mapudungun)", toponimia_fuente="https://es.wikipedia.org/wiki/Liqui%C3%B1e",
 fuentes=[tec("termas-rio-liquine-24"),U_SERN_XIV,U_ALAM,U_SANCHEZ,U_ELMOS_RIOS,"https://es.wikipedia.org/wiki/Liqui%C3%B1e"], notas="Valle de Liquiñe: 45 fuentes (Wikipedia). Alam 2010 agrupa 4 muestras 'Liquiñe' sin distinguir centro.")

add("Termas Manquecura", region="Los Ríos", comuna="Panguipulli", lat=-39.739093, lon=-71.845320, precision_coord="aprox", fuente_coord=tec("termas-manquecura-87"), tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="78 surgencia; piscinas 38-42", T_fuente_declarada="termasenchile.cl",
 infraestructura=["cabañas","piscinas","tinajas","camping","restaurante","spa"], categoria="medio", estado="operativa", barros="declarado", barro_detalle="barro termal (Sernatur 2012; termasenchile.cl)", propiedades_declaradas=["afecciones reumáticas"], pueblo_originario="Mapuche",
 fuentes=[tec("termas-manquecura-87"),U_SERN_XIV], notas="Km 34 camino Coñaripe-Liquiñe; gastronomía con influencia mapuche.")

add("Termas Punulaf", region="Los Ríos", comuna="Panguipulli", lat=-39.742295, lon=-71.843794, precision_coord="aprox", fuente_coord=tec("termas-punulaf-12"), tipo_manifestacion="manantial", origen_geologico=LOFZ, infraestructura=["tinajas","piscinas","cabañas","camping"], categoria="rústico", estado="operativa",
 pueblo_originario="Mapuche", fuentes=[tec("termas-punulaf-12")], notas="12 tinas; una de las principales de Liquiñe (Wikipedia).")

add("Termas Trafipán", alias=["Trafipan","Trifupán"], region="Los Ríos", comuna="Panguipulli", lat=-39.736253, lon=-71.858977, precision_coord="aprox", fuente_coord=tec("termas-trafipan-liquine-91"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="37.2 (Wrage 2017); 37 (Alam 2010 'Trifupán')", T_fuente_medida="Wrage et al. 2017 (TR); Alam et al. 2010", pH="8.7; 8.9", tipo_quimico="Na-Cl (Wrage); Na-SO4 (Alam)", iones_resumen="Alam: Na 60, Ca 9.8, Cl 23, SO4 77, HCO3 42, SiO2 42 mg/L; TDS 160",
 estudios=[WRAGE,ALAM], infraestructura=["piscinas","tinajas","cabañas","camping"], categoria="rústico", estado="operativa", barros="declarado", barro_detalle="1 baño de barro", pueblo_originario="Mapuche", fuentes=[tec("termas-trafipan-liquine-91"),U_WRAGE,U_ALAM], notas="200 m del camino principal en Liquiñe.")

add("Termas Rayenco", region="Los Ríos", comuna="Panguipulli", lat=-39.742084, lon=-71.844824, precision_coord="aprox", fuente_coord=tec("termas-rayenco-90"), tipo_manifestacion="manantial", origen_geologico=LOFZ, infraestructura=["piscinas","tinajas","cabañas","camping"], categoria="rústico", estado="operativa",
 barros="declarado", barro_detalle="2 baños de barro termal", pueblo_originario="Mapuche", fuentes=[tec("termas-rayenco-90")])

add("Termas Hipólito Muñoz", region="Los Ríos", comuna="Panguipulli", lat=-39.765152, lon=-71.793262, precision_coord="aprox", fuente_coord=tec("termas-hipolito-munoz-89"), tipo_manifestacion="manantial", origen_geologico=LOFZ, infraestructura=["piscinas","cabañas","camping"], categoria="rústico", estado="operativa",
 barros="declarado", barro_detalle="barro termal y baños de vapor 'torito'", pueblo_originario="Mapuche", fuentes=[tec("termas-hipolito-munoz-89")], notas="8 km de Liquiñe, ruta paso Carirriñe.")

add("Termas Carranco", alias=["Termas Carranco Huilo Huilo","Termas Huilo Huilo"], region="Los Ríos", comuna="Panguipulli", lat=-39.742251, lon=-71.849417, precision_coord="aprox", fuente_coord=tec("termas-carranco-huilo-huilo-16"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_declarada_C="~35 promedio", T_fuente_declarada="termasenchile.cl", infraestructura=["piscinas","camping","cabañas"], categoria="rústico", estado="operativa", operador="Reserva Biológica Huilo Huilo (fundo Carranco)", pueblo_originario="Mapuche",
 fuentes=[tec("termas-carranco-huilo-huilo-16"),tec("termas-huilo-huilo-116")], notas="7 km de Liquiñe, río Rañintulelfu; baño de vapor natural. Coordenada de la ficha 'Huilo Huilo' (-72.91) inválida.")

add("Termas Cofre", region="Los Ríos", comuna="Panguipulli", lat=-39.5065423, lon=-71.8906057, precision_coord="aprox", fuente_coord=tec("termas-cofre-117"), tipo_manifestacion="manantial", origen_geologico="volcánico (Villarrica) / "+LOFZ, infraestructura=["tinajas","piscinas","cabañas"], categoria="rústico", estado="operativa",
 pueblo_originario="Mapuche", fuentes=[tec("termas-cofre-117")], notas="Ladera sur volcán Villarrica, 15 km de Coñaripe.")

add("Termas Río Hueico", region="Los Ríos", comuna="Panguipulli", lat=-39.6941765, lon=-71.8958313, precision_coord="aprox", fuente_coord=tec("termas-rio-hueico-122"), tipo_manifestacion="manantial", origen_geologico=LOFZ, infraestructura=["pozones","tinajas","camping","restaurante"], categoria="rústico", estado="operativa",
 operador="Ecotour Coñaripe (contacto@ecotourconaripe.cl, +56 9 8466 5699)", pueblo_originario="Mapuche", fuentes=[tec("termas-rio-hueico-122")])

add("Termas Quilalelfu", alias=["Termas Quilalelfu - Coñaripe"], region="Los Ríos", comuna="Panguipulli", lat=-39.7300, lon=-71.8537, precision_coord="aprox", fuente_coord=tec("termas-quilalelfu-conaripe-106"), tipo_manifestacion="pozón", origen_geologico=LOFZ,
 infraestructura=["pozones","piscinas","restaurante"], categoria="rústico", estado="operativa", precio_declarado="2017-18: alta $10.000 adulto/$8.000 niño; baja $8.000/$5.000", pueblo_originario="Mapuche", toponimia="Quilalelfu = 'tres ríos' (mapudungun, según ficha)", toponimia_fuente=tec("termas-quilalelfu-conaripe-106"),
 fuentes=[tec("termas-quilalelfu-conaripe-106")], notas="Coordenada dudosa (cae cerca de Liquiñe aunque la ficha dice 7 min de Coñaripe).")

add("Eco Termas Pellaifa", alias=["Termas Pellaifa"], region="Los Ríos", comuna="Panguipulli", lat=-39.632059, lon=-71.927868, precision_coord="aprox", fuente_coord=tec("eco-termas-pellaifa-86"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C=50.0, T_fuente_medida="Wrage et al. 2017 (PF)", pH=8.0, tipo_quimico="Na-Cl (Wrage 2017)", T_declarada_C="35-40", T_fuente_declarada="termasenchile.cl", estudios=[WRAGE], infraestructura=["piscinas","tinajas","cabañas","restaurante"], categoria="medio", estado="operativa",
 barros="declarado", barro_detalle="piscina de barro termal", pueblo_originario="Mapuche", fuentes=[tec("eco-termas-pellaifa-86"),U_SERN_XIV,U_WRAGE])

add("Termas de Chihuío", alias=["Chihuio","Chihuío"], region="Los Ríos", comuna="Futrono", lat=-40.194302, lon=-71.936025, precision_coord="aprox", fuente_coord=tec("termas-de-chihuio-38"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="82.5 (Wrage 2017); 82 (Alam 2010); 82.4 (Sánchez & Alam 2009)", T_fuente_medida="Wrage et al. 2017 (CH); Alam et al. 2010; Sánchez & Alam 2009", pH="9.3-9.5", tipo_quimico="Na-Cl (Wrage); Na-SO4 (Alam)",
 iones_resumen="Alam 2010: Na 107, K 4.2, Ca 9.9, Cl 14, SO4 213, HCO3 25, SiO2 96 mg/L; TDS 450", estudios=[WRAGE,ALAM,SANCHEZ], infraestructura=["piscinas","tinajas","camping"], categoria="rústico", estado="operativa", operador="propietarios (familiar)", precio_declarado="'muy bajo costo'",
 indicaciones_historicas="Pablo Neruda se bañó aquí antes de su exilio de 1949 (termasenchile.cl)", pueblo_originario="Mapuche-Huilliche", fuentes=[tec("termas-de-chihuio-38"),U_SERN_XIV,U_WRAGE,U_ALAM], seguridad="Surgencia >80 °C", notas="Curso alto del río Curriñe, ~70 km de Futrono / 38 km de Llifén.")

add("Termas Río Florín", region="Los Ríos", comuna="Futrono", tipo_manifestacion="manantial", origen_geologico=LOFZ, T_medida_C=54.0, T_fuente_medida="Alam et al. 2010", pH=9.7, tipo_quimico="Na-SO4 (Alam 2010)", iones_resumen="Na 60, Ca 7.7, Cl 26, SO4 78, HCO3 26, SiO2 57 mg/L; TDS 180",
 estudios=[ALAM], estado="desconocido", pueblo_originario="Mapuche-Huilliche", fuentes=[U_ALAM], notas="Sin coordenadas ni info turística en fuentes consultadas.")

add("Termas Cerrillos", region="Los Ríos", comuna="Futrono", tipo_manifestacion="manantial", origen_geologico=LOFZ, T_medida_C="41; 32 (2 muestras)", T_fuente_medida="Alam et al. 2010", pH="9.4; 8.0", tipo_quimico="Na-SO4 (Alam 2010)", iones_resumen="Na 42-55, Ca 8-12, Cl 15-21, SO4 58-75, HCO3 29-47 mg/L; TDS 330",
 estudios=[ALAM], estado="desconocido", pueblo_originario="Mapuche-Huilliche", fuentes=[U_ALAM], notas="Sin coordenadas ni info turística en fuentes consultadas.")

add("Termas Llifén", alias=["Termas LLIFEN","Spa Termas Llifén"], region="Los Ríos", comuna="Futrono", lat=-40.205863, lon=-72.262752, precision_coord="aprox", fuente_coord=tec("termas-llifen-28"), tipo_manifestacion="NA", T_declarada_C="piscinas 20-40 (hidromasaje 36-38)", T_fuente_declarada="termasenchile.cl",
 infraestructura=["piscinas","spa","restaurante"], categoria="medio", estado="operativa", barros="declarado", barro_detalle="fangoterapia y mascarillas de barro (spa)", propiedades_declaradas=["calcio, azufre y minerales","afecciones cardiovasculares, hepáticas y reumáticas"], pueblo_originario="Mapuche-Huilliche",
 fuentes=[tec("termas-llifen-28"),U_SERN_XIV], notas="Centro spa en Llifén; origen del agua termal no documentado.")

# ================= LOS LAGOS =================
add("Termas de Puyehue", alias=["Hotel Termas de Puyehue","Puyehue Wellness & Spa Resort"], region="Los Lagos", comuna="Puyehue", lat=-40.711860, lon=-72.328285, precision_coord="exacta", fuente_coord="en.wikipedia.org/wiki/Puyehue_Hot_Springs", altitud_m="310 (Wikipedia en); ~275 (Wikipedia es)",
 tipo_manifestacion="manantial (5-7 vertientes)", origen_geologico="volcánico (Casablanca-Antillanca) / "+LOFZ, T_medida_C="60 (Wrage 2017); 60-65 promedio (Celis 2012)", T_fuente_medida="Wrage et al. 2017 (PU); Celis 2012", pH="8.3 (Wrage); 7-8.5 (Celis)",
 tipo_quimico="Na-Cl (Wrage); Na-Cl-SO4 (Celis)", iones_resumen="Geotermómetros 160-180 °C mínimo (Celis 2012)", T_declarada_C="41-54 (Wikipedia en); 24-75 en 7 vertientes (Risopatrón 1924)", T_fuente_declarada="Wikipedia", estudios=[WRAGE], tesis=[T_CELIS],
 infraestructura=["hotel","spa","piscinas","restaurante"], categoria="lujo", estado="operativa", administracion_comunitaria=False, web="https://www.puyehue.cl/", redes_sociales=[{"plataforma":"Facebook","url":"https://facebook.com/termas.puyehue","seguidores_aprox":"NA"},{"plataforma":"Instagram","url":"https://instagram.com/hoteltermaspuyehue","seguidores_aprox":"NA"},{"plataforma":"YouTube","url":"https://youtube.com/@hoteltermaspuyehue","seguidores_aprox":"NA"}],
 indicaciones_historicas="Descubiertas 1851 (H. Molina); sociedad 1907 (C. Hubach); hotel 1910; Gran Hotel 1939-1947; aguas alcalinas con depósito de yeso (Risopatrón 1924)", pueblo_originario="Huilliche (cultura Pitrén como antecesora, Wikipedia es)", uso_ancestral="pueblos originarios conocían sus propiedades (Wikipedia es)",
 area_protegida="Parque Nacional Puyehue", fuentes=["https://es.wikipedia.org/wiki/Termas_de_Puyehue","https://en.wikipedia.org/wiki/Puyehue_Hot_Springs","https://www.puyehue.cl/",U_SERN_X,U_WRAGE,U_CELIS], notas="Ruta 215 km 76. Propiedad pública/administración privada (Sernatur 2012).")

add("Termas Aguas Calientes (Puyehue)", alias=["Termas de Aguas Calientes"], region="Los Lagos", comuna="Puyehue", lat=-40.735378, lon=-72.307524, precision_coord="aprox", fuente_coord=tec("termas-aguas-calientes-26"), tipo_manifestacion="manantial; pozón de río", origen_geologico="volcánico (Casablanca-Antillanca) / "+LOFZ,
 T_medida_C=66.0, T_fuente_medida="Wrage et al. 2017 (AC)", pH=7.8, tipo_quimico="Na-Cl (Wrage); Na-Cl-SO4 (Celis 2012)", estudios=[WRAGE], tesis=[T_CELIS], infraestructura=["cabañas","piscinas","tinajas","camping","restaurante","spa"], categoria="medio", estado="operativa",
 administracion_comunitaria=False, web="https://www.termasaguascalientes.cl/", redes_sociales=[{"plataforma":"Instagram","url":"https://instagram.com/termasaguascalientes","seguidores_aprox":"NA"}], precio_declarado="pozones de río gratuitos (chile.travel)",
 propiedades_declaradas=["articulaciones","oxigenación","sistema inmunológico","'fuente curativa'"], pueblo_originario="Huilliche", area_protegida="Parque Nacional Puyehue (Reserva de la Biósfera)", fuentes=[tec("termas-aguas-calientes-26"),"https://www.termasaguascalientes.cl/",U_SERN_X,U_WRAGE,U_CELIS], notas="Río Chanleufú, camino a Antillanca km 4.")

add("Termas de Pangal", region="Los Lagos", comuna="Puyehue", tipo_manifestacion="manantial", origen_geologico=LOFZ, tipo_quimico="Na-Ca-Cl (Celis 2012)", tesis=[T_CELIS], estado="desconocido", pueblo_originario="Huilliche", fuentes=[U_CELIS], notas="~20 km al norte de Termas de Puyehue (Celis 2012). Sin coordenadas ni T.")

add("Termas de Rupanco", region="Los Lagos", comuna="Puyehue", tipo_manifestacion="manantial", origen_geologico=LOFZ, T_medida_C=80.0, T_fuente_medida="Wrage et al. 2017 (RU)", pH=7.9, tipo_quimico="Na-Cl (Wrage 2017)", estudios=[WRAGE], estado="desconocido", pueblo_originario="Huilliche", fuentes=[U_WRAGE],
 notas="Solo datos Wrage 2017; búsquedas de ubicación/infraestructura sin resultados.")

add("Cordón Caulle (Trahuilco / Los Baños)", alias=["Trahuilco","Los Baños","Géiseres del Caulle"], region="Los Lagos", comuna="Puyehue / Lago Ranco", tipo_manifestacion="géiser; fumarola; manantial", origen_geologico="volcánico (Cordón Caulle)", infraestructura=["ninguna"], categoria="natural", estado="desconocido",
 area_protegida="Parque Nacional Puyehue", seguridad="Campo geotermal activo; erupción 2011", fuentes=[U_SERN_XIV], notas="Sernatur Los Ríos 2012 menciona 'aguas termales y géiseres' en la ladera del volcán Puyehue. Tesis Sepúlveda (U. de Chile, repositorio 2250/126122) no accesible (bloqueo anti-bots). Sin datos medidos.")

add("Termas de Ralún", region="Los Lagos", comuna="Puerto Varas", lat=-41.363132, lon=-72.330696, precision_coord="aprox", fuente_coord=tec("termas-ralun-41"), tipo_manifestacion="manantial", origen_geologico=LOFZ, infraestructura=["cabañas","pozones"], categoria="rústico", estado="desconocido",
 pueblo_originario="Huilliche", area_protegida="Colindante Parque Nacional Vicente Pérez Rosales", fuentes=[tec("termas-ralun-41"),U_SERN_X], notas="Ribera NE del río Petrohué frente a Ralún; Sernatur 2012: baños al aire libre y cabañas, oct-mar, admin. público-privada.")

add("Termas El Callao", region="Los Lagos", comuna="Puerto Varas", lat=-40.977058, lon=-72.166615, precision_coord="aprox", fuente_coord=tec("termas-el-callao-40"), tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="39-42", T_fuente_declarada="termasenchile.cl",
 infraestructura=["tinajas"], categoria="rústico", estado="operativa", propiedades_declaradas=["bario, estroncio y manganeso (declarado)"], pueblo_originario="Huilliche", area_protegida="Parque Nacional Vicente Pérez Rosales", fuentes=[tec("termas-el-callao-40")], notas="Refugio entre lagos Todos los Santos y Rupanco; acceso a pie con operadores.")

add("Termas del Sol", region="Los Lagos", comuna="Cochamó", tipo_manifestacion="manantial", origen_geologico=LOFZ, T_declarada_C="36-45", T_fuente_declarada="El Mostrador 2020", infraestructura=["pozones","restaurante"], categoria="medio", estado="operativa", operador="Samuel del Sol y Jacinta León", administracion_comunitaria=False,
 web="https://termasdelsol.com", precio_declarado="$18.000 adulto; $12.000 niño (2020)", barros="declarado", barro_detalle="piscina de barro termal", pueblo_originario="Huilliche", noticias=[{"medio":"El Mostrador","anio":2020,"titulo":"Abre el primer centro termal de Puelo: Termas del Sol","link":U_ELMOS_SOL}],
 fuentes=[U_ELMOS_SOL], notas="Puelo; 10 pozones de piedra; abierto ~feb 2020. Sin coordenadas.")

add("Termas de Sotomó", alias=["Sotomo"], region="Los Lagos", comuna="Cochamó", lat=-41.660597, lon=-72.396681, precision_coord="aprox", fuente_coord=tec("termas-sotomo-32"), tipo_manifestacion="pozón intermareal", origen_geologico=LOFZ, T_declarada_C="37 superficie; 41 fondo", T_fuente_declarada="termasenchile.cl",
 infraestructura=["pozones","camping"], categoria="natural", estado="operativa", operador="colonos locales (alojamiento en casas)", administracion_comunitaria="NA", propiedades_declaradas=["~37 minerales, principalmente azufre (declarado)"], pueblo_originario="Huilliche",
 fuentes=[tec("termas-sotomo-32"),U_CT_AUSTRAL], notas="Estuario de Reloncaví, pozas visibles en marea baja.")

add("Termas de Pichicolo", region="Los Lagos", comuna="Hualaihué", lat=-41.97484, lon=-72.55288, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida; termasenchile.cl (-41.969879,-72.556249)", tipo_manifestacion="manantial", origen_geologico=LOFZ,
 tipo_quimico="Cl/SO4-Na, muy diluida (Hauser 1989)", estudios=[HAUSER], infraestructura=["pozones","restaurante"], categoria="medio", estado="operativa", web="https://www.termasdepichicolo.cl/", redes_sociales=[{"plataforma":"Instagram","url":"https://www.instagram.com/termaspichicolo/","seguidores_aprox":"NA"},{"plataforma":"Facebook","url":"https://www.facebook.com/termasdepichicolo","seguidores_aprox":"NA"}],
 precio_declarado="Mar-vie $29.000 adulto/$23.000 adulto mayor/$18.000 niño; fines de semana $32.000/$25.000/$21.000", propiedades_declaradas=["certificadas por MINSAL (declarado)","nitrato, sulfato, magnesio, hierro, zinc (declarado)"], indicaciones_historicas="Est. 1996 (web)", pueblo_originario="Huilliche",
 fuentes=["https://www.termasdepichicolo.cl/",tec("termas-de-pichicolo-105"),U_HAUSER,U_NOMADES], notas="Carretera Austral km 90, 9 km antes de Hornopirén; 6 pozones.")

add("Termas de Llancahué", alias=["Llancahue"], region="Los Lagos", comuna="Hualaihué", lat=-42.13371, lon=-72.5492, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida; termasenchile.cl (-42.022556,-72.691443)", tipo_manifestacion="manantial", origen_geologico=LOFZ,
 T_medida_C="58 (Waring 1965, citado en Hauser 1989)", T_fuente_medida="Hauser 1989", tipo_quimico="Cl/SO4-Na (Hauser 1989)", iones_resumen="Cl 1323, Na 655, Ca 222 mg/L; TDS 2366; depósitos de travertino", T_declarada_C="52 (tinas)", T_fuente_declarada="termasenchile.cl", estudios=[HAUSER],
 infraestructura=["hotel","tinajas","piscinas"], categoria="rústico", estado="operativa", pueblo_originario="Huilliche", fuentes=[U_HAUSER,tec("termas-de-llancahue-104")], notas="Isla Llancahué; Hauser 1989 la cita con instalaciones 'bien equipadas'.")

add("Termas de Cahuelmó", alias=["Cahuelmo"], region="Los Lagos", comuna="Hualaihué", lat=-42.2551, lon=-72.37597, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida; termasenchile.cl (-42.256681,-72.366213)", tipo_manifestacion="pozón", origen_geologico=LOFZ,
 T_medida_C="55 (Waring 1965, en Hauser 1989)", T_fuente_medida="Hauser 1989", tipo_quimico="HCO3-Na, alto Ca (Hauser 1989)", estudios=[HAUSER], infraestructura=["pozones","camping"], categoria="natural", estado="operativa", operador="Parque Pumalín (guardaparques en ene-feb; nomades.com)", administracion_comunitaria="NA",
 pueblo_originario="Huilliche", area_protegida="Parque Nacional Pumalín Douglas Tompkins", fuentes=[U_HAUSER,tec("termas-de-cahuelmo-103"),U_NOMADES], notas="Fiordo Cahuelmó, solo en lancha desde Hornopirén; reserva previa.")

add("Termas de Porcelana", region="Los Lagos", comuna="Chaitén", lat=-42.45595, lon=-72.44893, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida (coordenada de termasenchile.cl -42.916,-72.717 inconsistente)", tipo_manifestacion="manantial", origen_geologico=LOFZ,
 tipo_quimico="Cl/SO4-Na (Hauser 1989)", iones_resumen="Cl 846, SiO2 127 mg/L; TDS 1912", T_declarada_C="60", T_fuente_declarada="termasenchile.cl; nomades.com", estudios=[HAUSER], infraestructura=["piscinas","pozones","cabañas","camping","restaurante"], categoria="rústico", estado="operativa",
 barros="declarado", barro_detalle="baños de barro (termasenchile.cl)", pueblo_originario="Huilliche", fuentes=[U_HAUSER,tec("termas-de-porcelana-83"),U_NOMADES], notas="Fondo del fiordo Comau, acceso por mar + caminata 3 h.")

add("Termas El Amarillo", alias=["Termas del Amarillo","Refugio Termas El Amarillo"], region="Los Lagos", comuna="Chaitén", lat=-42.97579, lon=-72.40852, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida; termasenchile.cl (-43.0036,-72.4525)", tipo_manifestacion="manantial", origen_geologico="volcánico (Michinmahuida) / "+LOFZ,
 tipo_quimico="Cl/SO4-Na, muy diluida, pH alto (Hauser 1989)", pH="8.9-9.9 (grupo, Hauser 1989)", T_declarada_C="~52 promedio", T_fuente_declarada="Sernatur 2012", estudios=[HAUSER], infraestructura=["piscinas","pozones","cabañas","restaurante"], categoria="rústico", estado="operativa",
 precio_declarado="Refugio: $35.000 p/p con desayuno (termasenchile.cl)", barros="declarado", barro_detalle="sala de baño de barro (Sernatur 2012)", pueblo_originario="Huilliche", area_protegida="Entrada sur Parque Pumalín", fuentes=[U_HAUSER,U_SERN_X,tec("refugio-termas-el-amarillo-42"),tec("las-termas-el-amarillo-27")], notas="20 km al este de Chaitén; Hauser 1989 la clasifica entre las más calientes.")

add("Termas de Michinmahuida", region="Los Lagos", comuna="Chaitén", lat=-42.96453, lon=-72.38681, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida", tipo_manifestacion="manantial", origen_geologico="volcánico (Michinmahuida)", tipo_quimico="HCO3-Na, pH alto (Hauser 1989)", estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER])

for nm,(la,lo),ty,extra in [("Termas de Río Blanco (Hualaihué)",(-41.93831,-72.30883),"NA","ubicación aproximada según Hauser"),("Termas de Chilco",(-42.51577,-72.61465),"NA",""),("Termas El Peñón",(-42.60678,-72.5751),"Cl/SO4-Na, muy diluida",""),("Termas Lago Negro",(-42.73205,-72.59502),"Cl/SO4-Na, muy diluida",""),("Fuente mineral Yelcho",(-43.26512,-72.41944),"HCO3-Na (agua mineral carbonatada): CO2 194, Na 576, Ca 122-288, Mg 90, HCO3 ~1684-1914, Fe 5.9, Mn 2.5 mg/L; TDS 2210","fuente mineral, no termal"),("Termas de Moraga",(-43.34021,-72.40368),"HCO3-Na: Na 554 mg/L; TDS 1596",""),("Termas Santa Lucía",(-43.41983,-72.42844),"NA","")]:
    add(nm, region="Los Lagos", comuna="Chaitén" if "Hualaihué" not in nm else "Hualaihué", lat=la, lon=lo, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida", origen_geologico=LOFZ, tipo_quimico=ty if ty!="NA" and ":" not in ty else "NA", iones_resumen=ty if ":" in ty else "NA", estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER], notas="Registrada en Hauser 1989 (sin instalaciones). "+extra)

# ================= AYSÉN =================
AY_NOTE="Negri 2018 / Negri 2017 (tesis): grupos Na-Cl (borde de fiordo, CE >1000 µS/cm, pH neutro) y Na-Cl-HCO3 (interior, CE <1000, pH alcalino); mezcla con agua de fiordo 1.5-45 %. Datos por fuente no accesibles (PDF bloqueado)."
add("Termas de Puyuhuapi", alias=["Puyuhuapi Lodge & Spa","Termas de Puyuhuapi Lodge & Spa","Bahía Dorita"], region="Aysén", comuna="Cisnes", lat=-44.413727, lon=-72.645821, precision_coord="exacta", fuente_coord="hispanopedia/Wikipedia es Termas de Puyuhuapi; Hauser 1989 UTM (-44.41342,-72.64475)",
 tipo_manifestacion="manantial", origen_geologico=LOFZ+" (campo volcánico Puyuhuapi)", T_medida_C=">80 (manifestaciones superficiales, Allende 2017); 23-84 rango regional (Hauser 1989)", T_fuente_medida="Allende 2017; Hauser 1989", pH="neutro a levemente ácido (Allende 2017)",
 tipo_quimico="Na-Cl (Allende 2017; Negri 2018); Cl/SO4-Na (Hauser 1989)", iones_resumen="Hauser 1989: Cl 161, Ca 180, SO4 340-480 mg/L; TDS 1662", T_declarada_C="piscinas 30-42; interior 34; spa 47", T_fuente_declarada="Wikipedia es; chile.travel",
 estudios=[HAUSER,NEGRI], tesis=[T_ALLENDE,T_NEGRI], infraestructura=["hotel","spa","piscinas","restaurante"], categoria="lujo", estado="operativa", operador="Puyuhuapi Lodge & Spa (Eberhard Kossmann)", administracion_comunitaria=False, web="https://www.puyuhuapilodge.com/",
 propiedades_declaradas=["aguas bicarbonatadas con cloruro, sulfato, magnesio, cromo, zinc, selenio (declarado Wikipedia)"], indicaciones_historicas="Descubiertas por colono alemán Hopperdietzel; balneario fundado años 80 por Ernesto Hein; lodge 1986", barros="declarado", barro_detalle="pozo natural de barro (chile.travel)",
 fuentes=["https://es.hispanopedia.com/wiki/Termas_de_Puyuhuapi","https://www.puyuhuapilodge.com/",U_HAUSER,U_ALLENDE,U_NEGRIT,U_NEGRI,U_CT_AUSTRAL], notas=AY_NOTE)

add("Termas Ventisquero Puyuhuapi", alias=["Termas del Ventisquero"], region="Aysén", comuna="Cisnes", lat=-44.3716469, lon=-72.5762309, precision_coord="aprox", fuente_coord=tec("termas-ventisquero-puyuhuapi-119"), tipo_manifestacion="manantial", origen_geologico=LOFZ,
 pH="neutro a levemente ácido (Allende 2017)", tipo_quimico="Na-Cl (Allende 2017)", tesis=[T_ALLENDE], estudios=[NEGRI], T_declarada_C="35-44 (fuente); piscinas 20-40", T_fuente_declarada="termasenchile.cl", infraestructura=["piscinas","restaurante"], categoria="medio", estado="operativa", web="https://www.termasventisquero.cl/",
 area_protegida="Parque Nacional Queulat (según termasenchile.cl)", fuentes=[tec("termas-ventisquero-puyuhuapi-119"),U_ALLENDE], notas="6 km al sur de Puyuhuapi; web del operador bloqueada a robots. "+AY_NOTE)

add("Termas El Gañote", region="Aysén", comuna="Cisnes", tipo_manifestacion="manantial", origen_geologico=LOFZ, tipo_quimico="Na-Cl (Allende 2017)", tesis=[T_ALLENDE], estado="desconocido", fuentes=[U_ALLENDE], notas="Fuente cerca de Puerto Puyuhuapi muestreada por Allende 2017. Sin más datos.")

add("Termas de Queulat", region="Aysén", comuna="Cisnes", lat=-44.51601, lon=-72.54883, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida", tipo_manifestacion="manantial", origen_geologico=LOFZ, tipo_quimico="HCO3 dominante (Allende 2017)", estudios=[HAUSER], tesis=[T_ALLENDE],
 infraestructura=["ninguna"], categoria="natural", estado="desconocido", area_protegida="Parque Nacional Queulat (probable)", fuentes=[U_HAUSER,U_ALLENDE,U_CT_AUSTRAL], notas="Posada Queulat (km 192 Carretera Austral) ofrece tinajas (chile.travel) — relación con esta fuente no verificada.")

add("Termas Naturales El Sauce", alias=["Termas El Sauce"], region="Aysén", comuna="Cisnes", lat=-44.0292417, lon=-72.5332276, precision_coord="aprox", fuente_coord=tec("termas-naturales-el-sauce-118"), tipo_manifestacion="pozón", origen_geologico=LOFZ, infraestructura=["pozones"], categoria="rústico", estado="operativa",
 operador="Familia Berger", administracion_comunitaria=False, fuentes=[tec("termas-naturales-el-sauce-118")], notas="17 km de La Junta, camino a Raúl Marín Balmaceda; abre en verano. "+AY_NOTE)

add("Termas Puerto Bonito", region="Aysén", comuna="Cisnes", lat=-43.95382, lon=-72.72929, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida (coordenada de termasenchile.cl -45.93,-73.58 inconsistente)", tipo_manifestacion="manantial", origen_geologico="falla Yanteles-Mentolat (Hauser 1989)",
 T_declarada_C="45", T_fuente_declarada="termasenchile.cl", estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER,tec("termas-puerto-bonito-71")], notas="Río Palena, ruta a Raúl Marín km 31; Hauser 1989 la cita con instalaciones rústicas; hoy sin instalaciones (termasenchile.cl).")

add("Termas Valle Marta", region="Aysén", comuna="Cisnes", lat=-44.730730, lon=-72.683314, precision_coord="aprox", fuente_coord=tec("termas-valle-marta-72"), tipo_manifestacion="manantial de playa", origen_geologico=LOFZ, infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[tec("termas-valle-marta-72")],
 notas="Orilla oriental del canal Puyuhuapi; un lodge usa las aguas (ficha). Posible correspondencia con 'Trapananda' de Hauser 1989 (-44.754,-72.892 aprox). "+AY_NOTE)

add("Termas Quitralco", alias=["Quitralco Hot Springs","Termas de Quitralco"], region="Aysén", comuna="Aysén", lat=-45.667657, lon=-73.036851, precision_coord="aprox", fuente_coord=tec("quitralco-hot-springs-37")+" (UTM Hauser 1989 inconsistente)", tipo_manifestacion="manantial", origen_geologico=LOFZ,
 tipo_quimico="Cl/SO4-Na (Hauser 1989)", T_declarada_C="piscinas 32 y 38", T_fuente_declarada="termasenchile.cl", estudios=[HAUSER,NEGRI], infraestructura=["piscinas","hotel","restaurante"], categoria="lujo", estado="operativa", operador="Skorpios (solo pasajeros de cruceros)", administracion_comunitaria=False,
 fuentes=[U_HAUSER,tec("quitralco-hot-springs-37")], notas="Fiordo Quitralco; Hauser 1989 la describe con instalaciones entre las mejores. "+AY_NOTE)

add("Termas Puerto Pérez", alias=["Chilconal (Puerto Pérez) Hauser 1989"], region="Aysén", comuna="Aysén", lat=-45.405623, lon=-72.679779, precision_coord="aprox", fuente_coord=tec("termas-puerto-perez-69"), tipo_manifestacion="manantial costero", origen_geologico="volcánico (Macá) / "+LOFZ,
 infraestructura=["ninguna"], categoria="natural", estado="desconocido", area_protegida="Monumento Natural Cinco Hermanas", fuentes=[tec("termas-puerto-perez-69"),U_HAUSER], notas="Fiordo Aysén, 1 h de navegación desde Puerto Chacabuco; proyecto de piscinas flotantes. "+AY_NOTE)

add("Termas de Chilconal", region="Aysén", comuna="Aysén", lat=-45.4035437, lon=-72.6864154, precision_coord="aprox", fuente_coord=tec("termas-de-chilconal-120"), tipo_manifestacion="pozón", origen_geologico="volcánico (Macá-Cay) / "+LOFZ, tipo_quimico="Cl/SO4-Na (Hauser 1989 'Chilconal (Puerto Pérez)')",
 iones_resumen="SiO2 155 mg/L; TDS 1460 (Hauser 1989)", T_declarada_C="34-35", T_fuente_declarada="termasenchile.cl", estudios=[HAUSER,NEGRI], infraestructura=["ninguna"], categoria="natural", estado="operativa", propiedades_declaradas=["artritis y dolores reumáticos (declarado)"],
 fuentes=[tec("termas-de-chilconal-120"),U_HAUSER], notas="40 km al oeste de Puerto Aysén; temporada sep-mar. Hauser 1989 asigna UTM que corresponde a Ensenada Pérez (-45.237,-73.209): posible desalineación. "+AY_NOTE)

add("Termas Ensenada Pérez", region="Aysén", comuna="Aysén", lat=-45.2691281, lon=-73.2550395, precision_coord="aprox", fuente_coord=tec("termas-ensenada-perez-121"), tipo_manifestacion="manantial costero", origen_geologico="volcánico (Macá) / "+LOFZ, infraestructura=["ninguna"], categoria="natural", estado="desconocido",
 area_protegida="Monumento Natural Cinco Hermanas", fuentes=[tec("termas-ensenada-perez-121")], notas="Entrada del fiordo Aysén. Hotel Loberías del Sur (Puerto Chacabuco) ofrece piscinas a 40 °C y visitas a Cinco Hermanas (chile.travel). "+AY_NOTE)

add("Termas de Huemules", region="Aysén", comuna="Aysén", lat=-45.87879, lon=-73.29113, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida", origen_geologico=LOFZ, estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER], notas="Registrada en Hauser 1989 sin datos químicos.")
add("Termas de Cupquelán", alias=["Bahía Erasmo"], region="Aysén", comuna="Aysén", lat=-45.99537, lon=-73.39227, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida", origen_geologico=LOFZ, estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER], notas="Registrada en Hauser 1989 sin datos químicos.")
add("Termas de Huiña", region="Aysén", comuna="NA", lat=-46.31742, lon=-72.81328, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida (posible desalineación)", origen_geologico=LOFZ, estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER], notas="Registrada en Hauser 1989 sin datos químicos.")
add("Termas El Engaño", region="Aysén", comuna="NA", lat=-46.4542, lon=-72.7888, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida (posible desalineación)", origen_geologico=LOFZ, tipo_quimico="HCO3-Na, muy diluida, pH 8.9-9.9 (Hauser 1989)", estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER])
add("Termas Cristal", region="Aysén", comuna="NA", origen_geologico=LOFZ, estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER], notas="Hauser 1989: UTM N 4.839.110 (E no legible). Sin datos químicos.")
add("Termas Aeropuerto (Puyuhuapi)", region="Aysén", comuna="Cisnes", lat=-44.29161, lon=-72.61848, precision_coord="aprox", fuente_coord="UTM 18S Hauser 1989 convertida", origen_geologico=LOFZ, estudios=[HAUSER], infraestructura=["ninguna"], categoria="natural", estado="desconocido", fuentes=[U_HAUSER], notas="Registrada en Hauser 1989 sin datos químicos.")

# ================= MAGALLANES =================
add("Termas de Skyring", alias=["Aguas termales de Skyring","Punta Laura","La Pera"], region="Magallanes", comuna="Río Verde", tipo_manifestacion="manantial", origen_geologico="NA (cerca de volcanes marinos según carta geológica, CEQUA)", T_declarada_C=">50", T_fuente_declarada="CEQUA 2017 (Cequarito N°8)",
 tesis=[T_FELIU], estudios=[{"autor":"Feliú, D.","anio":2013,"titulo":"Termas de Skyring (memoria de arquitectura, propuesta turística)","tipo":"T","link":U_FELIU}], infraestructura=["ninguna"], categoria="natural", estado="desconocido", pueblo_originario="Kawésqar (ruta histórica, Feliú 2013)",
 fuentes=[U_FELIU,U_CEQUA], notas="Seno Skyring, ~127 km NO de Punta Arenas. Sin coordenadas ni química.")

add("Termas de Tierra del Fuego (Chile)", region="Magallanes", comuna="NA", estado="desconocido", notas="No se encontró ninguna fuente termal documentada en el sector chileno de Tierra del Fuego en las búsquedas realizadas (chile.travel, gochile, Wikipedia). Registro vacío a propósito.")

with open("/home/claude/thermalia_data/fichas_sur_austral.jsonl","w",encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps({k:r[k] for k in FIELDS},ensure_ascii=False)+"\n")

# resumen
def has(r,k): return r[k] not in ("NA",[],None)
print("n termas:",len(rows))
print("coords:",sum(1 for r in rows if has(r,"lat")))
print("T medida:",sum(1 for r in rows if has(r,"T_medida_C")))
print("quimica (tipo o iones):",sum(1 for r in rows if has(r,"tipo_quimico") or has(r,"iones_resumen")))
print("pH:",sum(1 for r in rows if has(r,"pH")))
print("infra (no ninguna):",sum(1 for r in rows if r["infraestructura"] and r["infraestructura"]!=["ninguna"]))
print("etnia:",sum(1 for r in rows if has(r,"pueblo_originario")))
print("web:",sum(1 for r in rows if has(r,"web")))
print("precio:",sum(1 for r in rows if has(r,"precio_declarado")))
from collections import Counter
print(Counter(r["region"] for r in rows))
