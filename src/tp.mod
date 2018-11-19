# CONJUNTOS

set DIAS;
set CANALES;
set HORAS;
set DEPORTES;
set SEDES;
set PERIODISTAS;
set EVENTOS;

# Definicion de Parametros

# Parametro M
param M;

# Parametro Auxiliar
param BLOQUES {h in HORAS};

# Parametros por deporte
param INTERCALABLE {d in DEPORTES};
param CALIDAD {d in DEPORTES};
param AUMENTO_ESPECIAL {d in DEPORTES};
param AUMENTO_FINAL {d in DEPORTES};
param PUEDE_CUBRIR {p in PERIODISTAS, d in DEPORTES};
param ESPECIALISTA {p in PERIODISTAS, d in DEPORTES};

# Parametros por eventos
param COMIENZO {e in EVENTOS};
param FIN {e in EVENTOS};
param DUR {e in EVENTOS};
param ES_FINAL {e in EVENTOS};
param ES_SEDE {e in EVENTOS, s in SEDES};
param DEP_EVENTO {e in EVENTOS, d in DEPORTES};
param DIAS_EVENTOS {e in EVENTOS, d in DIAS};

# Variables
#var tr{e in EVENTOS} >= 0, binary;
#var y{e in EVENTOS, j in JORNADA} >= 0, binary;

var t{e in EVENTOS} >=0, binary;
var y{e in EVENTOS, h in HORAS, c in CANALES, d in DIAS} >=0, binary;
var es_inter{e in EVENTOS} >=0, binary;
var intercal{e in EVENTOS, h in HORAS, c in CANALES, d in DIAS} >=0, binary;
var cubre{p in PERIODISTAS, e in EVENTOS, h in HORAS, d in DIAS} >=0, binary;
var cubierto{e in EVENTOS, p in PERIODISTAS} >=0, binary;
var asignado{d in DIAS, p in PERIODISTAS, s in SEDES} >=0, binary;
var especial{e in EVENTOS} >=0, binary;
var adm_sup{h in HORAS, c in CANALES, d in DIAS} >=0, binary;
var no_finales{d in DEPORTES} >=0, binary;
var es_especialista{p in PERIODISTAS, e in EVENTOS} >=0, binary;
var cub_esp{p in PERIODISTAS, e in EVENTOS} >=0, binary;
var en_canal{e in EVENTOS, c in CANALES} >=0, binary;

# Funcional

maximize z: sum{e in EVENTOS, d in DEPORTES} ( t[e] * DEP_EVENTO[e, d] * ( CALIDAD[d] + ES_FINAL[e] * AUMENTO_FINAL[d]) + DEP_EVENTO[e, d] * especial[e] * AUMENTO_ESPECIAL[d]);


################################################################################
#                                RESTRICCIONES                                 #
################################################################################


# Un bloque de evento no puede transmitirse en mas de un canal
s.t. un_canal {e in EVENTOS, h in HORAS, d in DIAS}: sum{c in CANALES} y[e, h, c, d] <= 1;

# Un evento no puede transmitirse un dia que no ocurra el evento
s.t. dia_evento {e in EVENTOS, h in HORAS, c in CANALES, d in DIAS}: y[e, h, c, d] <= DIAS_EVENTOS[e, d];

# Un evento no puede transmitirse en un bloque horario anterior a su bloque horario de comienzo
s.t. comienzo {e in EVENTOS, h in HORAS, c in CANALES, d in DIAS}: BLOQUES[h] >= COMIENZO[e] * y[e, h, c, d];

# Un evento no puede transmitirse en un bloque horario posterior a su bloque horario de finalizacion
s.t. fin {e in EVENTOS, h in HORAS, c in CANALES, d in DIAS}: FIN[e] >= (BLOQUES[h]+1) * y[e, h, c, d];

# Si un evento se transmite, todos sus bloques deben transmitirse
s.t. dur_inf {e in EVENTOS}: DUR[e] * t[e] <= sum{h in HORAS, c in CANALES, d in DIAS} y[e, h, c, d];
s.t. dur_sup {e in EVENTOS}: DUR[e] * t[e] >= sum{h in HORAS, c in CANALES, d in DIAS} y[e, h, c, d];

# En que canal se transmite un evento
s.t. canal_inf {e in EVENTOS, c in CANALES}: en_canal[e, c] <= sum{h in HORAS, d in DIAS} y[e, h, c, d];
s.t. canal_sup {e in EVENTOS, c in CANALES}: en_canal[e, c] * DUR[e] >= sum{h in HORAS, d in DIAS} y[e, h, c, d];

# Un evento entero no puede transmitirse en mas de un canal
s.t. un_canal_evt {e in EVENTOS}: sum{c in CANALES} en_canal[e, c] <= 1;

# En un determinado bloque horario, se pueden transmitir a lo sumo 2 eventos por canal en el caso de haber superposicion
s.t. super {h in HORAS, c in CANALES, d in DIAS}: sum{e in EVENTOS} y[e, h, c, d] <= adm_sup[h, c, d] + 1;

# Para que un evento admita superposicion, su deporte debe admitir superposicion
s.t. inter_inf {e in EVENTOS}: es_inter[e] <= sum{d in DEPORTES} INTERCALABLE[d] * DEP_EVENTO[e, d];
s.t. inter_sup {e in EVENTOS}: es_inter[e] >= sum{d in DEPORTES} INTERCALABLE[d] * DEP_EVENTO[e, d];

# Relaciono si un bloque-evento es intercalable con si su evento es intercalable
s.t. es_inter_inf {e in EVENTOS, h in HORAS, c in CANALES, d in DIAS}: 2 * intercal[e, h , c, d] <= y[e, h , c, d] + es_inter[e];
s.t. es_inter_sup {e in EVENTOS, h in HORAS, c in CANALES, d in DIAS}: intercal[e, h , c, d] +1 >= y[e, h , c, d] + es_inter[e];

# Para que un bloque admita superposicion, los eventos a transmitirse en dicho bloque deben ser intercalables
s.t. adm_sup_inf {h in HORAS, c in CANALES, d in DIAS}: 2 * adm_sup[h, c, d] <= sum{e in EVENTOS} intercal[e, h, c, d];
s.t. adm_sup_sup {h in HORAS, c in CANALES, d in DIAS}: adm_sup[h, c, d] + 1 >= sum{e in EVENTOS} intercal[e, h, c, d];

# Un evento es cubierto por a lo sumo un equipo periodistico
s.t. evt_un_p {e in EVENTOS, h in HORAS, d in DIAS}: sum{p in PERIODISTAS} cubre[p, e, h, d] <= 1;

# Un equipo periodistico cubre a lo sumo un evento
s.t. p_un_evt {p in PERIODISTAS, h in HORAS, d in DIAS}: sum{e in EVENTOS} cubre[p, e, h, d] <= 1;

# Si un bloque se transmite, debe ser cubierto por algun equipo
s.t. t_cubre {e in EVENTOS, h in HORAS, c in CANALES, d in DIAS}: y[e, h, c, d] <= sum{p in PERIODISTAS} cubre[p, e, h, d];

# Si el evento es cubierto, debe transmitirse en algun canal
s.t. cubre_t {e in EVENTOS, p in PERIODISTAS, h in HORAS, d in DIAS}: cubre[p, e, h, d] <= sum{c in CANALES} y[e, h, c, d];

# Relaciono con la variable que dice si un equipo cubre un evento
s.t. p_cubre_e_inf {e in EVENTOS, p in PERIODISTAS, d in DIAS}: cubierto[e, p] * DIAS_EVENTOS[e, d] <= sum{h in HORAS} cubre[p, e, h, d];
s.t. p_cubre_e_sup {e in EVENTOS, p in PERIODISTAS, d in DIAS}: M * cubierto[e, p] * DIAS_EVENTOS[e, d] >= sum{h in HORAS} cubre[p, e, h, d];

# Un evento solo debe ser cubierto por un equpo
s.t. un_e_un_p {e in EVENTOS}: sum{p in PERIODISTAS} cubierto[e, p] <= 1;

# Un equipo no puede cubrir un evento para el cual no esta habilitado
s.t. puede_cubrir { e in EVENTOS, p in PERIODISTAS}: cubierto[e, p] <= sum{d in DEPORTES} PUEDE_CUBRIR[p, d] * DEP_EVENTO[e, d];

# Debo saber si un equipo es especialista en un evento
s.t. p_es_esp_inf {e in EVENTOS, p in PERIODISTAS}: es_especialista[p, e] <= sum{d in DEPORTES} ESPECIALISTA[p, d] * DEP_EVENTO[e, d];
s.t. p_es_esp_sup {e in EVENTOS, p in PERIODISTAS}: es_especialista[p, e] >= sum{d in DEPORTES} ESPECIALISTA[p, d] * DEP_EVENTO[e, d];

# El beneficio lo tenemos si lo cubrimos y lo cubrimos por un especialista
s.t. cub_esp_inf {e in EVENTOS, p in PERIODISTAS}: 2 * cub_esp[p, e] <= cubierto[e, p] + es_especialista[p, e];
s.t. cub_esp_sup {e in EVENTOS, p in PERIODISTAS}: cub_esp[p, e] + 1 >= cubierto[e, p] + es_especialista[p, e];

# Entonces puedo decir si un evento es cubierto y es especial
s.t. cub_y_especial_inf {e in EVENTOS}: especial[e] <= sum{p in PERIODISTAS} cub_esp[p, e];
s.t. cub_y_especial_sup {e in EVENTOS}: especial[e] >= sum{p in PERIODISTAS} cub_esp[p, e];

# Un equipo no puede ser asignado a mas de una sede un mismo dia
s.t. p_una_sede {p in PERIODISTAS, d in DIAS}: sum{s in SEDES} asignado[d, p, s] <= 1;

# Un equipo solo puede cubrir eventos que ocurran la seda a la que estan asignados
s.t. p_cub_sede_inf {p in PERIODISTAS, d in DIAS, s in SEDES}: asignado[d, p, s] <= sum{e in EVENTOS} cubierto[e, p] * ES_SEDE[e, s] * DIAS_EVENTOS[e, d];
s.t. p_cub_sede_sup {p in PERIODISTAS, d in DIAS, s in SEDES}: asignado[d, p, s] * M >= sum{e in EVENTOS} cubierto[e, p] * ES_SEDE[e, s] * DIAS_EVENTOS[e, d];

# Quiero saber que deportes poseen eventos regulares (no finales)
s.t. no_final_inf {d in DEPORTES}: no_finales[d] <= sum{e in EVENTOS} DEP_EVENTO[e, d] * (1 - ES_FINAL[e]);
s.t. no_final_sup {d in DEPORTES}: no_finales[d] * M >= sum{e in EVENTOS} DEP_EVENTO[e, d] * (1 - ES_FINAL[e]);

# Para poder transmitir una final debo haber transmitido al menos un evento regular del mismo deporte
# Si el deporte no posee eventos regulares, puedo transmitir las finales igual
s.t. puedo_final {e in EVENTOS, d in DEPORTES}: t[e] * DEP_EVENTO[e, d] * ES_FINAL[e] <= ( sum{ee in EVENTOS} t[ee] * DEP_EVENTO[ee, d] * (1 - ES_FINAL[ee])) + (1 - no_finales[d]);

# Asimismo una final solo puede ser cubierta por un especialista
s.t. final_esp {e in EVENTOS}: t[e] * ES_FINAL[e] <= especial[e];

end;
