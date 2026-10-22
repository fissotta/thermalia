# Esquema común de registro por terma (JSON Lines, un objeto por línea, UTF-8)
Campos (usar "NA" si no se encontró; nunca inventar; cada dato con su fuente en `fuentes`):
id (slug ascii, ej. "termas-de-puyehue"), nombre, alias (lista), region, comuna, lat, lon, precision_coord ("exacta"|"aprox"|"NA"), fuente_coord,
altitud_m, tipo_manifestacion (manantial|pozón|géiser|fumarola|laguna|pozo|baño de barro|NA), origen_geologico (volcánico|falla Liquiñe-Ofqui|falla Pocuro|sedimentario|NA),
T_medida_C, T_fuente_medida, T_declarada_C, T_fuente_declarada, pH, CE_uS_cm, tipo_quimico (ej. "Na-Cl", "ácido-SO4", "Ca-HCO3"), iones_resumen, isotopos, caudal_L_s, As_mg_L,
n_estudios_FQ, n_estudios_G, n_estudios_B, n_estudios_Pel, n_estudios_T (enteros o "NA"), estudios (lista de {autor, anio, titulo, tipo, link}),
tesis (lista de {autor, anio, titulo, universidad, link}),
infraestructura (lista: hotel|cabañas|spa|piscinas|pozones|tinajas|camping|restaurante|ninguna), categoria (lujo|medio|rústico|natural|NA), estado (operativa|cerrada|desconocido),
operador, administracion_comunitaria (true|false|NA), web, redes_sociales (lista de {plataforma, url, seguidores_aprox}), precio_declarado,
barros (caracterizado|declarado|informal|ninguno|NA), barro_detalle, propiedades_declaradas (lista), indicaciones_historicas,
pueblo_originario, region_cultural, toponimia, toponimia_fuente, uso_ancestral,
noticias (lista de {medio, anio, titulo, link}), videos (lista de {plataforma, titulo, canal, link}),
area_protegida (nombre o "NA"), seguridad (notas: T ebullición, acidez, accidentes), fuentes (lista de links), notas.
