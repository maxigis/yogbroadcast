# CONJUNTOS

set DIAS;
set CANALES;
set HORAS;
set DEPORTES;
set SEDES;
set PERIODISTAS;
set EVENTOS;

# Definicion de Parametros

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

maximize z: sum{e in EVENTOS, d in DEPORTES} ( t[e] * DEP_EVENTO[e, d] * ( CALIDAD[e] + ES_FINAL[e] * AUMENTO_FINAL[d]) + DEP_EVENTO[e, d] * especial[e] * AUMENTO_ESPECIAL[d]);
